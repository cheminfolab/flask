import {
    Breadcrumb,
    BreadcrumbList,
} from "@/components/ui/breadcrumb"
import {
    SidebarTrigger,
} from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"
import { SearchForm } from "@/components/search-form"

import Layout, { Breadcrumbs } from "@/components/layout"
import ContainerSidebar from "@/components/containers-sidebar"

const ContainerPlaceholder = () => (
    <div className="flex flex-1 flex-col gap-4 p-4">
        {Array.from({ length: 24 }).map((_, index) => (
            <div key={index} className="bg-muted/50 aspect-video h-12 w-full rounded-lg" />
        ))}
    </div>
)

const ContainerHeader = () => (
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
                {name: "Containers", link: "/containers"},
            ]} />
        </BreadcrumbList>
        </Breadcrumb>
        <SearchForm className="w-full sm:ml-auto sm:w-auto" />
    </header>
)

const Containers = () => (
    <Layout
        header={<ContainerHeader />}
        auxSidebar={<ContainerSidebar />}
        children={<ContainerPlaceholder />}
    />
)

export default Containers