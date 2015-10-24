from skimage.feature import register_translation
from model.image.offset import Offsets
from model.image.stack import ImageStack
import logging

log = logging.getLogger(__name__)


class V1RegistrationAnalyzer(object):
    def determine_translation(self, image_stack: ImageStack, offsets: Offsets, brightfield_channel_name: str) -> Offsets:
        log.debug("Registering!")
        # We may only be partially done determining offsets. We'll pick up where we left off (or start at the beginning)
        assert len(image_stack) > 0
        assert len(offsets) <= image_stack.group_count
        if len(offsets) < image_stack.group_count:
            self._calculate_offsets(image_stack, offsets, brightfield_channel_name)
        return offsets

    def _calculate_offsets(self, image_stack: ImageStack, offsets: Offsets, channel: str):
        # We can't tell if the work is done, since we don't know how many of the images in image_stack are in the channel we want to use.
        # We know the absolute minimum
        first_image = self._get_first_out_of_focus_image(image_stack, channel)
        for unregistered_image in image_stack.filter(z_level=0, channel=channel, start=len(offsets)):
            x, y = self._calculate_translation(first_image, unregistered_image)
            offsets[unregistered_image.frame_number] = (x, y)
            log.debug("Registration for frame %s: x:%s, y%s" % (unregistered_image.frame_number, x, y))

    def _get_first_out_of_focus_image(self, image_stack: ImageStack, channel: str):
        for image in image_stack:
            if image.z_level == 0 and image.channel == channel:
                return image
        raise ValueError("Could not find an image to align the image stack against. You probably chose the wrong channel to do alignments with.")

    @staticmethod
    def _calculate_translation(base_image, uncorrected_image) -> (float, float):
        """
        Finds the translational offset required to align this image with all others in the stack.
        Returns dx, dy adjustments in pixels *but does not change the image!*

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
        left_dy, left_dx = register_translation(left_base_section, left_uncorrected, upsample_factor=20)[:2]
        right_dy, right_dx = register_translation(right_base_section, right_uncorrected, upsample_factor=20)[:2]
        #
        # # return the average of the left and right phase correlation corrections
        return (left_dx + right_dx) / 2.0, (left_dy + right_dy) / 2.0
