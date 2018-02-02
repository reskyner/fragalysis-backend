import os,sys
from .models import Target,Protein,Molecule,Compound
from .functions import NeutraliseCharges,desalt_compound
from django.core.exceptions import ValidationError
from rdkit import Chem
from rdkit.Chem import Lipinski
from rdkit.Chem import Descriptors

def add_target(title):
    """
    Add a target
    :param title:
    :return:
    """
    new_target = Target.objects.get_or_create(title=title)[0]
    return new_target

def add_prot(file_path,code,target):
    """
    Add a protein
    :param file_path:
    :param code:
    :param target_pk:
    :return:
    """
    new_prot = Protein.objects.get_or_create(code=code,target_id=target)[0]
    new_prot.apo_holo = True
    new_prot.pdb_info = file_path
    new_prot.save()
    return new_prot



def add_new_comp(mol, option=None, comp_id=None):
    """Function to add a new compound to the database given an RDKit molecule
    Takes an RDKit molecule. Option of LIG to return original smiles with the Compound object
    Returns a compound object for the RDKit molecule."""
    # Neutralise and desalt compound the compound
    s_store_mol = NeutraliseCharges(desalt_compound(Chem.MolToSmiles(mol, isomericSmiles=True)))[0]
    store_mol = Chem.MolFromSmiles(s_store_mol)
    if store_mol is None:
        sys.stderr.write("NEUTRALISING MADE NONE MOL" + " " + s_store_mol + " " + Chem.MolToSmiles(mol, isomericSmiles=True))
        return None
    # Store the isomeric smiles
    smiles = Chem.MolToSmiles(store_mol, isomericSmiles=True)
    # The inchi string is used for unique identification
    inchi = Chem.MolToInchi(store_mol)
    # Now convert back to inchi to canonicalise
    tmp_mol = Chem.MolFromInchi(inchi)
    if tmp_mol is None:
        # If error in INNCHI READ -> NOT NECCESARILY A KILLER
        sys.stderr.write("INCHI ERROR: " + inchi)
    else:
        inchi = Chem.MolToInchi(tmp_mol)
# Now attribute all this meta-deta to the compound object
    new_comp = Compound()
    new_comp.smiles = smiles
    if len(smiles) > Compound._meta.get_field('smiles').max_length:
        print "SMILES TOO LONG"
        return None
    new_comp.inchi = inchi
    m = store_mol
    try:
        new_comp.mol_log_p = Chem.Crippen.MolLogP(m)
    except:
        sys.stderr.write("NONE MOLECULE PRODUCED\n" + smiles + "\n" + inchi)
        return None
    new_comp.mol_wt = float(Chem.rdMolDescriptors.CalcExactMolWt(m))
    new_comp.heavy_atom_count = Chem.Lipinski.HeavyAtomCount(m)
    new_comp.heavy_atom_mol_wt = float(Descriptors.HeavyAtomMolWt(m))
    new_comp.nhoh_count = Chem.Lipinski.NHOHCount(m)
    new_comp.no_count = Chem.Lipinski.NOCount(m)
    new_comp.num_h_acceptors = Chem.Lipinski.NumHAcceptors(m)
    new_comp.num_h_donors = Chem.Lipinski.NumHDonors(m)
    new_comp.num_het_atoms = Chem.Lipinski.NumHeteroatoms(m)
    new_comp.num_rot_bonds = Chem.Lipinski.NumRotatableBonds(m)
    new_comp.num_val_electrons = Descriptors.NumValenceElectrons(m)
    new_comp.ring_count = Chem.Lipinski.RingCount(m)
    new_comp.tpsa = Chem.rdMolDescriptors.CalcTPSA(m)
    # Validate that the compound is unique
    try:
        new_comp.validate_unique()
        new_comp.save()
        if option is None:
            return new_comp
        elif option == "LIG":
            return (new_comp, smiles)
    except ValidationError:
        if option is None:
            return Compound.objects.get(inchi=inchi)
        elif option == "LIG":
            return (Compound.objects.get(inchi=inchi), smiles)

def add_mol(mol_sd,prot):

    rd_mol = Chem.MolFromMolFile(mol_sd)
    if rd_mol is None:
        return None
    # Get the reference compound
    comp_ref = add_new_comp(rd_mol)
    new_mol = Molecule.objects.get_or_create(prot_id=prot,comp_id=comp_ref)[0]
    # Make a protein object by which it is related in the DB
    new_mol.sdf_info = Chem.MolToMolBlock(rd_mol)
    new_mol.smiles = Chem.MolToSmiles(rd_mol, isomericSmiles=True)
    # Find out how to add this information from Proasis
    new_mol.lig_id = "LIG"
    new_mol.chain_id = "Z"
    new_mol.occupancy = 0.0
    # Add this to the compound list -> make sure this passes in for the
    # correct molecule. I.e. if it fails where does it go???
    # Now link that compound back
    new_mol.cmpd_id = comp_ref
    new_mol.save()
    return new_mol


def load_from_dir(target_name, dir_path):
    """
    Load the data for a given target from a directory structure
    :param target_name:
    :param dir_path:
    :return:
    """
    new_target = add_target(target_name)
    directories = os.listdir(dir_path)
    for xtal in directories:
        new_path = os.path.join(dir_path, xtal)
        new_prot = add_prot(os.path.join(new_path,xtal+"_apo.pdb"),xtal,new_target)
        new_mol = add_mol(os.path.join(new_path,xtal+".mol"), new_prot)
        if not new_mol:
            print("NONE MOL: "+xtal)