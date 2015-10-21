from skimage.feature import register_translation
from model.image.registration import RegistrationOffsets


class V1RegistrationAnalyzer(object):
    def determine_translation(self, image_stack, offsets: RegistrationOffsets, channel) -> RegistrationOffsets:
        # We may only be partially done determining offsets. We'll pick up where we left off (or start at the beginning)
        start_frame = self._get_start_frame(offsets, interval)
        if start_frame < len(image_stack):
            self._calculate_offsets(image_stack, start_frame, interval, offsets)
        return offsets

    def _calculate_offsets(self, image_stack, start_frame, interval, offsets):
        # we still have some work to do
        for image in image_stack[start_frame::interval]:
            skew = self._calculate_skew(image)
            offsets[image.frame_number] = skew

    @staticmethod
    def _determine_registration_offset(base_image, uncorrected_image):
        """
        Finds the translational offset required to align this image with all others in the stack.
        Returns dx, dy adjustments in pixels *but does not change the image!*
        :param base_image:   a 2D numpy array that the other image should be aligned to
        :param uncorrected_image:   a 2D numpy array
        :returns:   float, float
        """
        # Get the dimensions of the images that we're aligning
        base_height, base_width = base_image.shape
        uncorrected_height, uncorrected_width = uncorrected_image.shape

        # We take the area that roughly corresponds to the catch channels. This has two benefits: one, it
        # speeds up the registration significantly (as it scales linearly with image size), and two, if
        # a large amount of debris/yeast/bacteria/whatever shows up in the central trench, the registration
        # algorithm goes bonkers if it's considering that portion of the image.
        # Thus we separately find the registration for the left side and right side, and average them.
        left_base_section = base_image[:, base_width * 0.1: base_width * 0.3]
        left_uncorrected = uncorrected_image[:, uncorrected_width * 0.1: uncorrected_width * 0.3]
        right_base_section = base_image[:, base_width * 0.7: base_width * 0.9]
        right_uncorrected = uncorrected_image[:, uncorrected_width * 0.7: uncorrected_width * 0.9]

        # phase_correlate returns y, x instead of x, y, which is not the convention in scikit-image, so we reverse them
        # it also returns some error bars and other stuff we don't need, so we just take the first two items
        left_dy, left_dx = phase_correlate(left_base_section, left_uncorrected, upsample_factor=20)[:2]
        right_dy, right_dx = phase_correlate(right_base_section, right_uncorrected, upsample_factor=20)[:2]
        #
        # # return the average of the left and right phase correlation corrections
        return (left_dx + right_dx) / 2.0, (left_dy + right_dy) / 2.0