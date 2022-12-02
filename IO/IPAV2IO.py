from ipaPy2 import PeakMLIO
from ipaPy2 import ipa
import pandas as pd
import Logger as lg
import os


def generate_ipa_annotation(filepath):

    df = PeakMLIO.ReadPeakML(filepath)
    lg.log_error("A")
    DB=pd.read_csv(os.path.join(lg.current_directory,"FragmentDatabases","IPA_MS1.csv"))
    adducts=pd.read_csv(os.path.join(lg.current_directory,"FragmentDatabases","adducts.csv"))
    Bio=pd.read_csv(os.path.join(lg.current_directory,"FragmentDatabases","allBIO_reactions.csv"))

    lg.log_error(df.head())

    lg.log_error("B")
    annotations = ipa.simpleIPA(df=df,ionisation=1,DB=DB,adductsAll=adducts,ppm=3,ppmthr=5,Bio=Bio,
                                delta_add=0.1,delta_bio=0.1,burn=1000,noits=5000,ncores=70)

    lg.log_error("C")

    PeakMLIO.add_IPA_to_PeakML(filepath, annotations, filepath)