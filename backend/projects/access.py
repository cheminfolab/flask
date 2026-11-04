"""
Access rules for projects and experiments, expressed as query conditions so
that list endpoints, detail endpoints and the per-row `can_edit` flag all use
the same logic.

Experiments
  read:  author, members of the experiment's working group, admins (read only),
         members with an experiment share (read/edit), the project owner,
         members with a project share (read/edit)
  edit:  author, members with an *edit* share on the experiment or its project.
         Admins can read everything but edit nothing they were not given.
  lock / sharing: only the author completes an experiment and manages its shares.

Projects
  read:  owner, members of the project's working group, admins,
         members with a project share
  edit:  owner, members with an *edit* project share (edit = change project
         details and create experiments in it). Only the owner manages shares.
"""
from django.db.models import BooleanField, Exists, ExpressionWrapper, OuterRef, Q, Value

from .models import AccessLevel, ExperimentShare, ProjectShare


def _project_share(user, project_ref, edit=False):
    shares = ProjectShare.objects.filter(project=project_ref, member=user)
    if edit:
        shares = shares.filter(level=AccessLevel.EDIT)
    return Q(Exists(shares))


def _experiment_share(user, edit=False):
    shares = ExperimentShare.objects.filter(experiment=OuterRef('pk'), member=user)
    if edit:
        shares = shares.filter(level=AccessLevel.EDIT)
    return Q(Exists(shares))


def project_read_condition(user):
    if user.is_staff:
        return Q()
    condition = Q(owner=user) | _project_share(user, OuterRef('pk'))
    if user.working_group_id:
        condition |= Q(working_group_id=user.working_group_id)
    return condition


def project_edit_condition(user):
    return Q(owner=user) | _project_share(user, OuterRef('pk'), edit=True)


def experiment_read_condition(user):
    if user.is_staff:
        return Q()
    condition = (
        Q(owner=user)
        | Q(project__owner=user)
        | _experiment_share(user)
        | _project_share(user, OuterRef('project_id'))
    )
    if user.working_group_id:
        condition |= Q(working_group_id=user.working_group_id)
    return condition


def experiment_edit_condition(user):
    return (
        Q(owner=user)
        | _experiment_share(user, edit=True)
        | _project_share(user, OuterRef('project_id'), edit=True)
    )


def _flag(condition):
    return ExpressionWrapper(condition, output_field=BooleanField()) if condition else Value(True)


def readable_projects(queryset, user):
    """Projects the user may read, each annotated with `can_edit`."""
    return queryset.filter(project_read_condition(user)).annotate(can_edit=_flag(project_edit_condition(user)))


def readable_experiments(queryset, user):
    """Experiments the user may read, each annotated with `can_edit`."""
    return queryset.filter(experiment_read_condition(user)).annotate(
        can_edit=_flag(experiment_edit_condition(user))
    )


def can_edit_experiment(user, experiment):
    """For objects not loaded through readable_experiments()."""
    if hasattr(experiment, 'can_edit'):
        return experiment.can_edit
    model = type(experiment)
    return model.objects.filter(pk=experiment.pk).filter(experiment_edit_condition(user)).exists()


def can_read_experiment(user, experiment):
    model = type(experiment)
    return model.objects.filter(pk=experiment.pk).filter(experiment_read_condition(user)).exists()


def can_edit_project(user, project):
    if hasattr(project, 'can_edit'):
        return project.can_edit
    model = type(project)
    return model.objects.filter(pk=project.pk).filter(project_edit_condition(user)).exists()
