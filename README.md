## PeakMLViewerPy - Version 0.4.0
***
## Using packaged release

Release consists of zipped folder PeakMLViewerPy_0_4_0.

Releases are currently available for for Windows 10 v2004 64-bit, MacOS Catalina and Linux Ubuntu v20.04.

Executable requires MoleculeDatabases folder and settings.xml file stored at same root, which is how the files are packaged.

Errors and user actions are written to .txt log file at root.
***
## Running source locally

Source can be run in Python with the following third-party libraries installed.

- rdata
- ttkwidgets
- image
- lxml
- faker
- pyreadr
- scipy
- molmass

***
## Compiling from source (Windows)

1. Install latest version of miniconda.
2. Run the following:
```
mkdir Source
cd Source
sudo apt install git
git clone https://github.com/UoMMIB/PeakMLViewerPy
cd PeakMLViewerPy

# Set up virtual environment to install libraries (required for rdkit)

conda create -c conda-forge -n peakml_env rdkit
conda activate peakml_env
pip install rdata
pip install ttkwidgets
pip install image
pip install lxml
pip install faker
pip install pyreadr
pip install scipy
pip install molmass
pip install pyinstaller

pyinstaller PeakMLViewerPy_oswin.spec
```

Executable file available in dist folder.
***
## Packag from source (macOS)

1. Install latest version of miniconda (https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html).
2. Run the following to initialise miniconda.
```
    source miniconda3/bin/activate
    conda init zsh
    conda init
```

3. Run the following as bash script in location for install:
```
# Create the following folder in the homw
mkdir Source
cd Source

# Check if git is already installed. If you don’t have it installed already, the following command will prompt you to install it.
git --version 

git clone https://github.com/UoMMIB/PeakMLViewerPy
cd PeakMLViewerPy

# Set up virtual environment to install libraries (required for rdkit)

conda create -c conda-forge -n peakml_env rdkit
conda activate peakml_env
pip install rdata
pip install ttkwidgets
pip install image
pip install lxml
pip install faker
pip install pyreadr
pip install scipy
pip install molmass
pip install pyinstaller
pip uninstall numpy
pip install numpy

pyinstaller PeakMLViewerPy_osmac.spec

cp settings.xml dist/PeakMLViewerPy
cp -r MoleculeDatabases dist/PeakMLViewerPy
cp -r FragmentDatabases dist/PeakMLViewerPy
```

Executable file available in dist/PeakMLViewerPy folder.
***
## Compiling from source (Linux)

1. Install latest version of miniconda.
2. Run the following commands in sequence in the location for install:
```
mkdir Source
cd Source
sudo apt install git
sudo apt-get install -y binutils libc6
git clone https://github.com/UoMMIB/PeakMLViewerPy
cd PeakMLViewerPy

# Set up virtual environment to install libraries (required for rdkit)

conda create -c conda-forge -n peakml_env rdkit
conda activate peakml_env
pip install rdata
pip install ttkwidgets
pip install image
pip install lxml
pip install faker
pip install pyreadr
pip install scipy
pip install molmass
pip install pyinstaller

pyinstaller PeakMLViewerPy_oslinux.spec

cp settings.xml dist
cp -r MoleculeDatabases dist
cp -r FragmentDatabases dist/PeakMLViewerPy
```
Can be run by clicking binary file available in dist folder.
***

## Using the IPA integration

This is the process to use the application with Integrated Probabilistic Analysis:

IPA is described in this paper:
Francesco Del Carratore, Kamila Schmidt, Maria Vinaixa, Katherine A Hollywood, Caitlin Greenland-Bews, Eriko Takano, Simon Rogers, and Rainer Breitling. Integrated Probabilistic Annotation: A Bayesian-Based Annotation Method for Metabolomic Profiles Integrating Biochemical Connections, Isotope Patterns, and Adduct Relationships. Analytical Chemistry, 91(20):12799–12807, 2019. ISSN 15206882. doi:10.1021/acs.analchem.9b02354.

With the source available here:
https://github.com/francescodc87/IPA

The PeakMLViewerPy application has two methods for integrating with this process.

To get the IPA identification for the currently import PeakML file with the PeakMLViewerPy, under 'IPA' menu item select 'Export entries as IPA input'.

Then to run the IPA process, first install it using the process described in its own GitHub page.
Then run this script with the output from the PeakMLViewerPy replacing "example_input.RData".

```
data("isotopes")
data("adducts")

# Update these with appropriate values
ionisation="positive" 
ppm=10

# Load the data from the PeakMLViewerPy output, and seperate it into the required parameter data objects.
load("example_input.RData")
entries_dataset <- sapply(dataset[1:3], as.numeric)
entries_relation_id <- as.vector(dataset[4])
entries_id <- sapply(as.vector(dataset[5]), as.character)

# Then run the multistage IPA process

Hits <- find.hits(adducts.matrix= all_adducts_POS,
                 dataset=entries_dataset,
                 ppm.thr= 5*ppm,
                 RTwin=60,
                 relation.id = entries_relation_id,
                 isotopes=isotopes,
                 iso.threshold=1)

Prior <- compute.Priors(Hits=Hits, dataset=entries_dataset,
                        pk=rep(1,nrow(Hits$all.formulas)),
                        ppm=ppm,unknown.ppm = 3*ppm, pr.lim = 1e-15)

### building ADD matrix
ADD <- build.add.connenctivity.matrix(Prior=Prior,  DB=DB,
                                      ionisation,fully.connected=FALSE)

### building ISO matrix
ISO <- build.iso.connectivity.matrix(Prior=Prior, DB=DB, ratios=TRUE)

### building BIO matrix
BIO1 <- build.bio.connectivity.matrix(Prior=Prior, DB=DB,
                                      ionisation,
                                      connection.type="reactions")
                                      
Post <- IPAposteriors(P=Prior,
                      Iso = ISO, 
                      Add = ADD, 
                      Bio = BIO1,
                      Int = as.numeric(entries_dataset[,3]),
                      ratio.toll = 0.8,
                      delta.iso = .1, 
                      delta.add = .1, 
                      delta.bio = 1,
                      allsamp = T, 
                      no.its = 5000, 
                      burn = 1000,
                      rel.id = entries_relation_id)

Final.res <- ParseIPAresults(Post, Prior, dataset=entries_dataset, DB = DB, IDs=entries_id)

# This last stage outputs a format that can be read by 

options("encoding" = "UTF-8")
save(Final.res, file = "example_output.RData")
```

The resulting output file can be imported into the PeakMLViewerPy via the 'IPA' menu item, 'Import IPA results'.
This will shown the identifications found by it in the Identifications View widget, and by saving the PeakML file, will include these there.
