# voronoi-mapper
Plot a series of places on a map in the style of a Voronoi diagram, based on an input csv file formatted in the following style (columns in this order - the column header names do not matter):

| Labels / Places | Y-Coord / Latitude | X-Coord / Longitude | Colour Place / Been to Place |
|:---------------:|:------------------:|:-------------------:|:----------------------------:|
|     England     |            52.3555 |             -1.1743 |               Y              |
|   Isle of Man   |            54.2361 |             -4.5481 |               N              |
|    N Ireland    |            54.7877 |             -6.4923 |               N              |
|     Scotland    |            56.4907 |             -4.2026 |               Y              |
|      Wales      |            52.1307 |             -3.7837 |               Y              |

## Step 1: Clone `voronoi-mapper` repo
Clone the `voronoi-mapper` repo to your area. Note you may need to set up ssh keys and add them to your GitHub account first, see [here](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

```bash
git clone git@github.com:GluonicPenguin/voronoi-mapper.git
```

## Step 2: Install requirements

`voronoi-mapper` uses a conda installer, with the conda environment set up in Miniconda. To set up Miniconda3 and install the mapper requirements, do the following:

```bash
MINICONDA_DIR=/path/to/miniconda3 # change this to somewhere outside the voronoi-mapper repo
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $MINICONDA_DIR # this creates the miniconda3 directory at the known /path/to
rm Miniconda3-latest-Linux-x86_64.sh

source $MINICONDA_DIR/etc/profile.d/conda.sh
conda update -y -n base -c defaults conda
export PYTHONNOUSERSITE=true
```

Then back in your `voronoi-mapper` directory, set up the environment:

```bash
conda env create -f mapper_env_requirements.yml
conda activate voronoi_mapper_env
```

## Step 3: Use mapper

`voronoi-mapper` takes two positional arguments: the input csv file and the output file name and path. An optional argument for the output plot type, e.g. pdf or png, is available (default is pdf). For example:

```
python voronoi_mapper.py /path/to/places.csv /path/for/places_plot
```

The result should look like the following:

![Alt text](examples/place_plot.png?raw=true "Default example of places")


