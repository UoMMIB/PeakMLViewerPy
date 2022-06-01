from Data.View.BaseItem import BaseItem

class IdentificationItem(BaseItem):
    def __init__(self, id: int, formula: str = "", ppm: str = "", adduct: str = "", name: str = "", class_desc: str = "", description: str = "", prior: str = "", post: str = "", smiles: str = "", inchi: str = "", notes: str = "", IPA_id: str = "", IPA_name: str = "", IPA_formula: str = "", IPA_adduct: str = "", IPA_mz: str = "", IPA_charge: str = "", IPA_ppm: str = "", IPA_isotope_pattern_score: str = "", IPA_fragmentation_pattern_score: str = "", IPA_prior: str = "", IPA_post: str = "", IPA_post_Gibbs: str = "", IPA_post_chi_square_pval: str = "", IPA_smiles: str = "", IPA_inchi: str = ""):
        super().__init__()

        self.id = id
        self.formula = formula
        self.ppm = ppm
        self.adduct = adduct
        self.name = name
        self.class_desc = class_desc
        self.description = description
        self.prior = prior
        self.post = post
        self.smiles = smiles
        self.inchi = inchi
        self.notes = notes
        self.IPA_id = IPA_id
        self.IPA_name = IPA_name
        self.IPA_formula = IPA_formula
        self.IPA_adduct = IPA_adduct
        self.IPA_mz = IPA_mz
        self.IPA_charge = IPA_charge
        self.IPA_ppm = IPA_ppm
        self.IPA_isotope_pattern_score = IPA_isotope_pattern_score
        self.IPA_fragmentation_pattern_score = IPA_fragmentation_pattern_score
        self.IPA_prior = IPA_prior
        self.IPA_post = IPA_post
        self.IPA_post_Gibbs = IPA_post_Gibbs
        self.IPA_post_chi_square_pval = IPA_post_chi_square_pval
        self.IPA_smiles = IPA_smiles
        self.IPA_inchi = IPA_inchi

        self.prior_modified = False

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def formula(self) -> str:
        return self._formula

    @formula.setter
    def formula(self, formula: str):
        self._formula = formula

    @property
    def ppm(self) -> float:
        return self._ppm

    @ppm.setter
    def ppm(self, ppm: float):
        self._ppm = ppm

    @property
    def adduct(self) -> str:
        return self._adduct

    @adduct.setter
    def adduct(self, adduct: str):
        self._adduct = adduct

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def class_desc(self) -> str:
        return self._class_desc

    @class_desc.setter
    def class_desc(self, class_desc: str):
        self._class_desc = class_desc

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def prior(self) -> float:
        return self._prior

    @prior.setter
    def prior(self, prior: float):
        self._prior = prior

    @property
    def post(self) -> float:
        return self._post

    @post.setter
    def post(self, post: float):
        self._post = post

    @property
    def smiles(self) -> str:
        return self._smiles

    @smiles.setter
    def smiles(self, smiles: str):
        self._smiles = smiles

    @property
    def inchi(self) -> str:
        return self._inchi

    @inchi.setter
    def inchi(self, inchi: str):
        self._inchi = inchi

    @property
    def notes(self) -> str:
        return self._notes

    @notes.setter
    def notes(self, notes: str):
        self._notes = notes

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

    @property
    def prior_modified(self) -> bool:
        return self._prior_modified

    @prior_modified.setter
    def prior_modified(self, prior_modified: bool):
        self._prior_modified = prior_modified
