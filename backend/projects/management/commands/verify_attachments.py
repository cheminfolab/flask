import hashlib

from django.core.management.base import BaseCommand, CommandError

from projects.models import Attachment


class Command(BaseCommand):
    help = (
        "Check that every attachment file exists and matches the SHA-256 checksum recorded "
        "at upload. Run it after restoring a backup. Exits with an error if any file is "
        "missing or altered."
    )

    def handle(self, *args, **options):
        missing, altered, checked = [], [], 0
        for attachment in Attachment.objects.order_by('uploaded_at').iterator():
            checked += 1
            storage, name = attachment.file.storage, attachment.file.name
            if not storage.exists(name):
                missing.append(attachment)
                continue
            digest = hashlib.sha256()
            with storage.open(name, 'rb') as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b''):
                    digest.update(chunk)
            if digest.hexdigest() != attachment.sha256:
                altered.append(attachment)

        for label, items in (('MISSING', missing), ('ALTERED', altered)):
            for attachment in items:
                self.stderr.write(
                    f"{label}: {attachment.id} '{attachment.original_name}' (experiment {attachment.experiment_id})"
                )
        if missing or altered:
            raise CommandError(f"{len(missing)} missing and {len(altered)} altered of {checked} attachments.")
        self.stdout.write(self.style.SUCCESS(f"All {checked} attachments present and intact."))
