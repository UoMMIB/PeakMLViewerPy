from typing import List

class IPAParams:

    def __init__(self):
        self.ionisation = 1
        self.ppm = 1
        self.noits = 100
        self.burn = None
        self.delta_add = None
        self.delta_bio = None
        self.mode ='reactions'
        self.CSunk = 0.5
        self.isodiff = 1
        self.ppmiso = 100
        self.ncores = 1
        self.me = float(5.48579909065e-04)
        self.ratiosd = 0.9
        self.ppmunk = None
        self.ratiounk = None
        self.ppmthr = None
        self.pRTNone = None
        self.pRTout = None
        self.mzdCS = 0
        self.ppmCS = 10
        self.evfilt = False
        self.connections = ["C3H5NO", "C6H12N4O", "C4H6N2O2", "C4H5NO3",
                             "C3H5NOS", "C6H10N2O3S2","C5H7NO3","C5H8N2O2",
                             "C2H3NO","C6H7N3O","C6H11NO","C6H11NO","C6H12N2O",
                             "C5H9NOS","C9H9NO","C5H7NO","C3H5NO2","C4H7NO2",
                             "C11H10N2O","C9H9NO2","C5H9NO","C4H4O2","C3H5O",
                             "C10H12N5O6P","C10H15N2O3S","C10H14N2O2S","CH2ON",
                             "C21H34N7O16P3S","C21H33N7O15P3S","C10H15N3O5S",
                             "C5H7","C3H2O3","C16H30O","C8H8NO5P","CH3N2O",
                             "C5H4N5","C10H11N5O3","C10H13N5O9P2",
                             "C10H12N5O6P","C9H13N3O10P2","C9H12N3O7P",
                             "C4H4N3O","C10H13N5O10P2","C10H12N5O7P","C5H4N5O",
                             "C10H11N5O4","C10H14N2O10P2","C10H12N2O4",
                             "C5H5N2O2","C10H13N2O7P","C9H12N2O11P2",
                             "C9H11N2O8P","C4H3N2O2","C9H10N2O5","C2H3O2",
                             "C2H2O","C2H2","CO2","CHO2","H2O","H3O6P2","C2H4",
                             "CO","C2O2","H2","O","P","C2H2O","CH2","HPO3",
                             "NH2","PP","NH","SO3","N","C6H10O5",
               "C6H10O6","C5H8O4","C12H20O11","C6H11O8P","C6H8O6","C6H10O5",
               "C18H30O15"]

    @property
    def ionisation(self) -> int:
        return self._ionisation

    @ionisation.setter
    def ionisation(self, ionisation: int):
        if ionisation is None:
            self._ionisation = None
        else:
            self._ionisation = int(ionisation)

    # Accuracy of the MS instrument used
    @property
    def ppm(self) -> float:
        return self._ppm

    @ppm.setter
    def ppm(self, ppm: float):
        if ppm is None:
            self._ppm = None
        else:
            self._ppm = float(ppm)

    # number of iterations if the Gibbs sampler to be run
    @property
    def noits(self) -> float:
        return self._noits

    @noits.setter
    def noits(self, noits: float):
        if noits is None:
            self._noits = None
        else:
            self._noits = float(noits)

    # number of iterations to be ignored when computing posterior
    # probabilities. If None, is set to 10% of total iterations
    @property
    def burn(self) -> int:
        return self._burn

    @burn.setter
    def burn(self, burn: int):
        if burn is None:
            self._burn = None
        else:
            self._burn = int(burn)

    # parameter used when computing the conditional priors. The
    # parameter must be positive. The smaller the parameter the more
    # weight the adducts connections have on the posterior
    # probabilities. Default 1.
    @property
    def delta_add(self) -> float:
        return self._delta_add

    @delta_add.setter
    def delta_add(self, delta_add: float):
        self._delta_add = delta_add
        if delta_add is None:
            self._delta_add = 1
        else:
            self._delta_add = float(delta_add)

    # parameter used when computing the conditional priors.
    # The parameter must be positive. The smaller the parameter the
    #more weight the adducts connections have on the posterior
    # probabilities. Default 1.
    @property
    def delta_bio(self) -> float:
        return self._delta_bio

    @delta_bio.setter
    def delta_bio(self, delta_bio: float):
        if delta_bio is None:
            self._delta_bio = 1
        else:
            self._delta_bio = float(delta_bio)

    # either 'reactions' (connections are computed based on the reactions
    # present in the database) or 'connections' (connections are computed
    # based on the list of connections provided). Default 'reactions'.
    @property
    def mode(self) -> str:
        return self._mode

    @mode.setter
    def mode(self, mode: str):
        self._mode = mode

    # cosine similarity score associated with the 'unknown' annotation.
    # Default 0.7 
    @property
    def CSunk(self) -> float:
        return self._CSunk

    @CSunk.setter
    def CSunk(self, CSunk: float):
        if CSunk is None:
            self._CSunk = None
        else:
            self._CSunk = float(CSunk)

    # Default value 1. Difference between isotopes of charge 1, does not
    # need to be exact
    @property
    def isodiff(self) -> float:
        return self._isodiff

    @isodiff.setter
    def isodiff(self, isodiff: float):
        if isodiff is None:
            self._isodiff = None
        else:
            self._isodiff = float(isodiff)

    # Default value 100. Maximum ppm value allowed between 2 isotopes.
    # It is very high on purpose
    @property
    def ppmiso(self) -> float:
        return self._ppmiso

    @ppmiso.setter
    def ppmiso(self, ppmiso: float):
        if ppmiso is None:
            self._ppmiso = None
        else:
            self._ppmiso = float(ppmiso)

    # default value 1. Number of cores used
    @property
    def ncores(self) -> float:
        return self._ncores

    @ncores.setter
    def ncores(self, ncores: float):
        if ncores is None:
            self._ncores = None
        else:
            self._ncores = float(ncores)

    # accurate mass of the electron. Default 5.48579909065e-04
    @property
    def me(self) -> float:
        return self._me

    @me.setter
    def me(self, me: float):
        if me is None:
            self._me = None
        else:
            self._me = float(me)

    # default 0.9. It represents the acceptable ratio between predicted
    # floatensity and observed floatensity of isotopes. it is used to compute
    # the shape parameters of the lognormal distribution used to
    # calculate the isotope pattern scores as sqrt(1/ratiosd)
    @property
    def ratiosd(self) -> float:
        return self._ratiosd

    @ratiosd.setter
    def ratiosd(self, ratiosd: float):
        if ratiosd is None:
            self._ratiosd = None
        else:
            self._ratiosd = float(ratiosd)

    # ppm associated to the 'unknown' annotation. If not provided equal
    # to ppm.
    @property
    def ppmunk(self) -> float:
        return self._ppmunk

    @ppmunk.setter
    def ppmunk(self, ppmunk: float):
        if ppmunk is None:
            self._ppmunk = None
        else:
            self._ppmunk = float(ppmunk)

    # isotope ratio associated to the 'unknown' annotation. If not
    # provided equal to 0.5
    @property
    def ratiounk(self) -> float:
        return self._ratiounk

    @ratiounk.setter
    def ratiounk(self, ratiounk: float):
        if ratiounk is None:
            self._ratiounk = None
        else:
            self._ratiounk = float(ratiounk)

    # Maximum ppm possible for the annotations. Ff not provided equal to
    # 2*ppm
    @property
    def ppmthr(self) -> float:
        return self._ppmthr

    @ppmthr.setter
    def ppmthr(self, ppmthr: float):
        if ppmthr is None:
            self._ppmthr = None
        else:
            self._ppmthr = float(ppmthr)

    # Multiplicative factor for the RT if no RTrange present in the
    # database. If not provided equal to 0.8
    @property
    def pRTNone(self) -> float:
        return self._pRTNone

    @pRTNone.setter
    def pRTNone(self, pRTNone: float):
        if pRTNone is None:
            self._pRTNone = None
        else:
            self._pRTNone = float(pRTNone)

    # Multiplicative factor for the RT if measured RT is outside the
    # RTrange present in the database. If not provided equal to 0.4
    @property
    def pRTout(self) -> float:
        return self._pRTout

    @pRTout.setter
    def pRTout(self, pRTout: float):
        if pRTout is None:
            self._pRTout = None
        else:
            self._pRTout = float(pRTout)

    # Maximum mz difference allowed when computing cosine similarity
    # scores. If one wants to use this parameter instead of ppmCS, this
    # must be set to 0. Default 0.
    @property
    def mzdCS(self) -> float:
        return self._mzdCS

    @mzdCS.setter
    def mzdCS(self, mzdCS: float):
        if mzdCS is None:
            self._mzdCS = None
        else:
            self._mzdCS = float(mzdCS)

    # Maximum ppm allowed when computing cosine similarity scores.
    # If one wants to use this parameter instead of mzdCS, this must be
    # set to 0. Default 10.
    @property
    def ppmCS(self) -> float:
        return self._ppmCS

    @ppmCS.setter
    def ppmCS(self, ppmCS: float):
        if ppmCS is None:
            self._ppmCS = None
        else:
            self._ppmCS = float(ppmCS)

    #evfilt: Default value False. If true, only spectra acquired with the same
    # collision energy are considered.

    @property
    def evfilt(self) -> bool:
        return self._evfilt

    @evfilt.setter
    def evfilt(self, evfilt: bool):
        self._evfilt = evfilt

    # list of possible connections between compounds defined as
    # formulas. Only necessary if mode='connections'. A list of
    # common biotransformations is provided as default.
    @property
    def connections(self) -> List[str]:
        return self._connections

    @connections.setter
    def connections(self, connections: List[str]):
        self._connections = connections
