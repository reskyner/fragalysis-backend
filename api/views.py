from xchem_db.models import (
    Crystal,
    DataProcessing,
    Dimple,
    Lab,
    Refinement,
    PanddaAnalysis,
    PanddaRun,
    PanddaSite,
    PanddaEvent,
    ProasisOut,
)
from xchem_db.serializers import (
    CrystalSerializer,
    DataProcessingSerializer,
    DimpleSerializer,
    LabSerializer,
    RefinementSerializer,
    PanddaAnalysisSerializer,
    PanddaRunSerializer,
    PanddaSiteSerializer,
    PanddaEventSerializer,
    ProasisOutSerializer,
)

from .security import ISpyBSafeQuerySet


class CrystalView(ISpyBSafeQuerySet):
    paginate_by = None
    queryset = Crystal.objects.filter()
    filter_permissions = "visit__proposal"
    serializer_class = CrystalSerializer
    filter_fields = (
        "crystal_name",
        "target__target_name",
        "compound__smiles",
        "visit__filename",
        "visit__proposal__proposal",
        "visit__visit",
    )


class DataProcessingView(ISpyBSafeQuerySet):
    paginate_by = None
    queryset = DataProcessing.objects.filter()
    filter_permissions = "crystal__visit__proposal"
    serializer_class = DataProcessingSerializer
    filter_fields = (
        "crystal_name__crystal_name",
        "crystal_name__target__target_name",
        "crystal_name__compound__smiles",
        "crystal_name__visit__filename",
        "crystal_name__visit__proposal__proposal",
        "crystal_name__visit__visit",
    )


class DimpleView(ISpyBSafeQuerySet):
    paginate_by = None
    queryset = Dimple.objects.filter()
    filter_permissions = "crystal__visit__proposal"
    serializer_class = DimpleSerializer
    filter_fields = (
        "crystal_name__crystal_name",
        "crystal_name__target__target_name",
        "crystal_name__compound__smiles",
        "crystal_name__visit__filename",
        "crystal_name__visit__proposal__proposal",
        "crystal_name__visit__visit",
        "reference__reference_pdb",
    )


class LabView(ISpyBSafeQuerySet):
    paginate_by = None
    queryset = Lab.objects.filter()
    filter_permissions = "crystal__visit__proposal"
    serializer_class = LabSerializer
    filter_fields = (
        "crystal_name__crystal_name",
        "crystal_name__target__target_name",
        "crystal_name__compound__smiles",
        "crystal_name__visit__filename",
        "crystal_name__visit__proposal__proposal",
        "crystal_name__visit__visit",
        "data_collection_visit",
        "library_name",
        "library_plate",
    )


class RefinementView(ISpyBSafeQuerySet):
    paginate_by = None
    queryset = Refinement.objects.filter()
    filter_permissions = "crystal__visit__proposal"
    serializer_class = RefinementSerializer
    filter_fields = (
        "crystal_name__crystal_name",
        "crystal_name__target__target_name",
        "crystal_name__compound__smiles",
        "crystal_name__visit__filename",
        "crystal_name__visit__proposal__proposal",
        "crystal_name__visit__visit",
        "outcome",
    )


class PanddaAnalysisView(ISpyBSafeQuerySet):
    paginate_by = None
    queryset = PanddaAnalysis.objects.filter()
    filter_permissions = "crystal__visit__proposal"
    serializer_class = PanddaAnalysisSerializer
    filter_fields = ("pandda_dir",)


class PanddaRunView(ISpyBSafeQuerySet):
    paginate_by = None
    queryset = PanddaRun.objects.filter()
    filter_permissions = "crystal__visit__proposal"
    serializer_class = PanddaRunSerializer
    filter_fields = (
        "input_dir",
        "pandda_analysis__pandda_dir",
        "pandda_log",
        "pandda_version",
        "sites_file",
        "events_file",
    )


class PanddaSiteView(ISpyBSafeQuerySet):
    paginate_by = None
    queryset = PanddaSite.objects.filter()
    filter_permissions = "crystal__visit__proposal"
    serializer_class = PanddaSiteSerializer
    filter_fields = (
        "pandda_run__pandda_analysis__pandda_dir",
        "pandda_run__pandda_log",
        "pandda_run__pandda_sites_file",
        "pandda_run__pandda_events_file",
        "pandda_run__input_dir",
        "site",
    )


class PanddaEventView(ISpyBSafeQuerySet):
    paginate_by = None
    queryset = PanddaEvent.objects.filter()
    filter_permissions = "crystal__visit__proposal"
    serializer_class = PanddaEventSerializer
    filter_fields = (
        "crystal__crystal_name",
        "crystal__target__target_name",
        "crystal__compound__smiles",
        "crystal__visit__filename",
        "crystal__visit__proposal__proposal",
        "crystal__visit__visit",
        "pandda_run__pandda_analysis__pandda_dir",
        "pandda_run__pandda_log",
        "pandda_run__pandda_sites_file",
        "pandda_run__pandda_events_file",
        "pandda_run__input_dir",
        "site__site",
        "event",
        "lig_id",
        "pandda_event_map_native",
        "pandda_model_pdb",
        "pandda_input_mtz",
        "pandda_input_pdb",
    )


class ProasisOutView(ISpyBSafeQuerySet):
    paginate_by = None
    queryset = ProasisOut.objects.filter()
    filter_permissions = "crystal__visit__proposal"
    serializer_class = ProasisOutSerializer
    filter_fields = (
        "crystal__crystal_name",
        "crystal__target__target_name",
        "crystal__compound__smiles",
        "crystal__visit__filename",
        "crystal__visit__proposal__proposal",
        "crystal__visit__visit",
        "proasis__strucid",
        "proasis__crystal_name__crystal_name",
        "proasis__crystal_name__target__target_name",
        "proasis__crystal_name__compound__smiles",
        "proasis__crystal_name__visit__filename",
        "proasis__crystal_name__visit__proposal__proposal",
        "proasis__crystal_name__visit__visit",
        "proasis__refinement__crystal_name__crystal_name",
        "proasis__refinement__crystal_name__target__target_name",
        "proasis__refinement__crystal_name__compound__smiles",
        "proasis__refinement__crystal_name__visit__filename",
        "proasis__refinement__crystal_name__visit__proposal__proposal",
        "proasis__refinement__crystal_name__visit__visit",
        "proasis__refinement__outcome",
        "root",
        "start",
    )
