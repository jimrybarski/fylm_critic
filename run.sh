if [ -z $1 ]; then
    echo ""
    echo "Error! You need to specify the directory where the image files are located."
    echo ""
    echo "Example:  ./run.sh /home/susie/experimental_data/150421"
    echo ""
else
    experiment_directory="$@" make shell
fi
