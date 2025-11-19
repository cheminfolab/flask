import { 
    SidebarInset,
    SidebarProvider,
    SidebarTrigger 
} from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"
import { 
    Breadcrumb, 
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator
} from "./ui/breadcrumb"

import { AppSidebar } from "@/components/app-sidebar"
import { SearchForm } from "@/components/search-form"
import { useState } from "react"

const Layout = ({ children, auxSidebar }: { children: React.ReactNode, auxSidebar?: React.ReactNode }) => {
    const [open, setOpen] = useState(true)

    return(
        <SidebarProvider open={open} onOpenChange={setOpen}>
            <AppSidebar />
            <SidebarInset>
                <header className="sticky top-0 flex shrink-0 items-center gap-2 px-4 h-16 border-b bg-background w-full">
                    <SidebarTrigger />
                    <Separator
                        orientation="vertical"
                        className="mr-2 h-4"
                    />
                    <Breadcrumb>
                        <BreadcrumbList>
                        <BreadcrumbItem className="hidden md:block">
                            <BreadcrumbLink href="#">Home</BreadcrumbLink>
                        </BreadcrumbItem>
                        <BreadcrumbSeparator className="hidden md:block" />
                        <BreadcrumbItem>
                            <BreadcrumbPage>Projects</BreadcrumbPage>
                        </BreadcrumbItem>
                        </BreadcrumbList>
                    </Breadcrumb>
                    <SearchForm className="w-full sm:ml-auto sm:w-auto" />
                </header>
                {children}
            </SidebarInset>
            {auxSidebar}
        </SidebarProvider>
    )
}

export default Layout