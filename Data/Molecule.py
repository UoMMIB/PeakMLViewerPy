class Molecule:

    def __init__(self, database_id: str, name: str, formula: str):
        self.database_id = database_id
        self.name = name
        self.formula = formula
        self.mass = None
        self.inchi = None
        self.smiles = None
        self.description = None
        self.class_description = None
        self.synonyms = None
        self.retention_time = None
        self.polarity = None
        self.IPA_id = None
        self.IPA_name = None
        self.IPA_formula = None
        self.IPA_adduct = None
        self.IPA_mz = None
        self.IPA_charge = None
        self.IPA_ppm = None
        self.IPA_isotope_pattern_score = None
        self.IPA_fragmentation_pattern_score = None
        self.IPA_prior = None
        self.IPA_post = None
        self.IPA_post_Gibbs = None
        self.IPA_post_chi_square_pval = None


    @property
    def database_id(self) -> str:
        return self._database_id

    @database_id.setter
    def database_id(self, database_id: str):
        self._database_id = database_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def formula(self) -> str:
        return self._formula

    @formula.setter
    def formula(self, formula: str):
        self._formula = formula

    @property
    def mass(self) -> str:
        return self._mass

    @mass.setter
    def mass(self, mass: str):
        self._mass = mass

    @property
    def inchi(self) -> str:
        return self._inchi

    @inchi.setter
    def inchi(self, inchi: str):
        self._inchi = inchi

    @property
    def smiles(self) -> str:
        return self._smiles

    @smiles.setter
    def smiles(self, smiles: str):
        self._smiles = smiles

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def class_description(self) -> str:
        return self._class_description

    @class_description.setter
    def class_description(self, class_description: str):
        self._class_description = class_description

    @property
    def synonyms(self) -> str:
        return self._synonyms

    @synonyms.setter
    def synonyms(self, synonyms: str):
        self._synonyms = synonyms

    @property
    def retention_time(self) -> float:
        return self._retention_time

    @retention_time.setter
    def retention_time(self, retention_time: float):
        self._retention_time = retention_time

    @property
    def polarity(self) -> str:
        return self._polarity

    @polarity.setter
    def polarity(self, polarity: str):
        self._polarity = polarity

    @property
    def IPA_id(self) -> str:
        return self._IPA_id

    @IPA_id.setter
    def IPA_id(self, IPA_id: str):
        self._IPA_id = IPA_id

    @property
    def IPA_name(self) -> str:
        return self._IPA_name

    @IPA_name.setter
    def IPA_name(self, IPA_name: str):
        self._IPA_name = IPA_name

    @property
    def IPA_formula(self) -> str:
        return self._IPA_formula

    @IPA_formula.setter
    def IPA_formula(self, IPA_formula: str):
        self._IPA_formula = IPA_formula

    @property
    def IPA_adduct(self) -> str:
        return self._IPA_adduct

    @IPA_adduct.setter
    def IPA_adduct(self, IPA_adduct: str):
        self._IPA_adduct = IPA_adduct

    @property
    def IPA_mz(self) -> str:
        return self._IPA_mz

    @IPA_mz.setter
    def IPA_mz(self, IPA_mz: str):
        self._IPA_mz = IPA_mz

    @property
    def IPA_charge(self) -> str:
        return self._IPA_charge

    @IPA_charge.setter
    def IPA_charge(self, IPA_charge: str):
        self._IPA_charge = IPA_charge

    @property
    def IPA_ppm(self) -> str:
        return self._IPA_ppm

    @IPA_ppm.setter
    def IPA_ppm(self, IPA_ppm: str):
        self._IPA_ppm = IPA_ppm

    @property
    def IPA_isotope_pattern_score(self) -> str:
        return self._IPA_isotope_pattern_score

    @IPA_isotope_pattern_score.setter
    def IPA_isotope_pattern_score(self, IPA_isotope_pattern_score: str):
        self._IPA_isotope_pattern_score = IPA_isotope_pattern_score

    @property
    def IPA_fragmentation_pattern_score(self) -> str:
        return self._IPA_fragmentation_pattern_score

    @IPA_fragmentation_pattern_score.setter
    def IPA_fragmentation_pattern_score(self, IPA_fragmentation_pattern_score: str):
        self._IPA_fragmentation_pattern_score = IPA_fragmentation_pattern_score

    @property
    def IPA_prior(self) -> str:
        return self._IPA_prior

    @IPA_prior.setter
    def IPA_prior(self, IPA_prior: str):
        self._IPA_prior = IPA_prior

    @property
    def IPA_post(self) -> str:
        return self._IPA_post

    @IPA_post.setter
    def IPA_post(self, IPA_post: str):
        self._IPA_post = IPA_post

    @property
    def IPA_post_Gibbs(self) -> str:
        return self._IPA_post_Gibbs

    @IPA_post_Gibbs.setter
    def IPA_post_Gibbs(self, IPA_post_Gibbs: str):
        self._IPA_post_Gibbs = IPA_post_Gibbs

    @property
    def IPA_post_chi_square_pval(self) -> str:
        return self._IPA_post_chi_square_pval

    @IPA_post_chi_square_pval.setter
    def IPA_post_chi_square_pval(self, IPA_post_chi_square_pval: str):
        self._IPA_post_chi_square_pval = IPA_post_chi_square_pval

    @property
    def IPA_smiles(self) -> str:
        return self._IPA_smiles

    @IPA_smiles.setter
    def IPA_smiles(self, IPA_smiles: str):
        self._IPA_smiles = IPA_smiles

    @property
    def IPA_inchi(self) -> str:
        return self._IPA_inchi

    @IPA_inchi.setter
    def IPA_inchi(self, IPA_inchi: str):
        self._IPA_inchi = IPA_inchi
