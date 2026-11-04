import { SearchForm } from "@/components/search-form"
import { Breadcrumb, BreadcrumbList } from "@/components/ui/breadcrumb"
import { Separator } from "@/components/ui/separator"
import { SidebarTrigger } from "@/components/ui/sidebar"

import Layout, { Breadcrumbs } from "@/components/layout"

const DashboardPlaceholder = () => (
    <div className="flex flex-1 flex-col gap-4 p-4">
        <div className="grid auto-rows-min gap-4 md:grid-cols-3">
        <div className="bg-muted/50 aspect-video rounded-xl" />
        <div className="bg-muted/50 aspect-video rounded-xl" />
        <div className="bg-muted/50 aspect-video rounded-xl" />
        </div>
        <div className="bg-muted/50 min-h-screen flex-1 rounded-xl md:min-h-min" />
    </div>
)

const HomeHeader = () => (
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
            ]} />
        </BreadcrumbList>
        </Breadcrumb>
        <SearchForm className="w-full sm:ml-auto sm:w-auto" />
    </header>
)

const Home = () => (
    <Layout
        children={<DashboardPlaceholder />}
        header={<HomeHeader />}
    />
)

export default Home