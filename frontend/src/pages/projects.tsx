import { useEffect, useState, type FormEventHandler } from "react"
import { FolderClosed, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Empty,
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/ui/empty"
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"
import { Breadcrumb, BreadcrumbList } from "@/components/ui/breadcrumb"
import { SearchForm } from "@/components/search-form"

import Layout, { Breadcrumbs } from "@/components/layout"
import useAxios from "@/hooks/useAxios"
import { errorMessage } from "@/lib/api"
import type { Project, ProjectRequest } from "@/types/api"

const ProjectsHeader = ({onCreate}: {onCreate: () => void}) => (
    <header className="sticky top-0 flex shrink-0 items-center gap-2 px-4 h-16 border-b bg-background w-full">
        <SidebarTrigger />
        <Separator
            orientation="vertical"
            className="mr-2 h-4"
        />
        <Breadcrumb>
        <BreadcrumbList>
          <Breadcrumbs items={[
            {name: "Home", link: "/"},
            {name: "Projects", link: "/projects"},
          ]} />
        </BreadcrumbList>
        </Breadcrumb>
        <div className="ml-auto flex items-center gap-2">
            <SearchForm className="w-full sm:w-auto" />
            <Button size="sm" onClick={onCreate}><Plus /> New project</Button>
        </div>
    </header>
)

const EmptyProject = ({onCreate}: {onCreate: () => void}) => (
  <Empty>
    <EmptyHeader>
      <EmptyMedia variant="icon">
        <FolderClosed />
      </EmptyMedia>
      <EmptyTitle>No Projects Yet</EmptyTitle>
      <EmptyDescription>
        You haven&apos;t created any projects yet.
        Get started by creating your first project.
      </EmptyDescription>
    </EmptyHeader>
    <EmptyContent className="flex-row justify-center gap-2">
      <Button onClick={onCreate}>Create Project</Button>
    </EmptyContent>
  </Empty>
)

type CreateProjectDialogProps = {
    open: boolean
    onOpenChange: (open: boolean) => void
    onCreated: (project: Project) => void
}

const CreateProjectDialog = ({open, onOpenChange, onCreated}: CreateProjectDialogProps) => {
    const api = useAxios()
    const [error, setError] = useState<string | null>(null)
    const [saving, setSaving] = useState(false)

    const handleSubmit: FormEventHandler<HTMLFormElement> = event => {
        event.preventDefault()
        const data = new FormData(event.currentTarget)
        const body: ProjectRequest = {
            title: String(data.get("title") ?? "").trim(),
            description: String(data.get("description") ?? "").trim(),
        }
        setSaving(true)
        setError(null)
        api.create<Project>("projects", body)
            .then(project => {
                onCreated(project)
                onOpenChange(false)
            })
            .catch(err => setError(errorMessage(err)))
            .finally(() => setSaving(false))
    }

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent>
                <form onSubmit={handleSubmit}>
                    <DialogHeader>
                        <DialogTitle>New project</DialogTitle>
                        <DialogDescription>
                            Members of your working group can read it. You can share it with others later.
                        </DialogDescription>
                    </DialogHeader>
                    <FieldGroup className="py-4">
                        <Field>
                            <FieldLabel htmlFor="project-title">Title</FieldLabel>
                            <Input id="project-title" name="title" required maxLength={200} />
                        </Field>
                        <Field>
                            <FieldLabel htmlFor="project-description">Description</FieldLabel>
                            <Input id="project-description" name="description" />
                        </Field>
                        {error ? <FieldError>{error}</FieldError> : null}
                    </FieldGroup>
                    <DialogFooter>
                        <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
                        <Button type="submit" disabled={saving}>{saving ? "Creating…" : "Create"}</Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    )
}

const ProjectList = ({projects}: {projects: Project[]}) => (
    <div className="grid gap-4 p-4 md:grid-cols-2 xl:grid-cols-3">
        {projects.map(project => (
            <Card key={project.id}>
                <CardHeader>
                    <CardTitle>{project.title}</CardTitle>
                    <CardDescription>
                        {project.description || "No description"}
                        <br />
                        Created {new Date(project.created_at).toLocaleDateString()}
                        {project.can_edit ? "" : " · read only"}
                    </CardDescription>
                </CardHeader>
            </Card>
        ))}
    </div>
)

const Projects = () => {
    const api = useAxios()
    const [projects, setProjects] = useState<Project[] | null>(null)
    const [error, setError] = useState<string | null>(null)
    const [creating, setCreating] = useState(false)

    useEffect(() => {
        api.getAll<Project>("projects")
            .then(setProjects)
            .catch(err => {
                setProjects([])
                setError(errorMessage(err))
            })
    }, [api])

    const openCreate = () => setCreating(true)

    let content
    if (projects === null) content = null  // loading
    else if (error) content = <p role="alert" className="text-destructive p-4 text-sm">{error}</p>
    else if (projects.length === 0) content = <EmptyProject onCreate={openCreate} />
    else content = <ProjectList projects={projects} />

    return(
        <Layout header={<ProjectsHeader onCreate={openCreate} />}>
            {content}
            <CreateProjectDialog
                open={creating}
                onOpenChange={setCreating}
                onCreated={project => setProjects(current => [project, ...(current ?? [])])}
            />
        </Layout>
    )
}

export default Projects
