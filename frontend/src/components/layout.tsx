import { Fragment, useContext, useEffect, useState } from "react"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"
import { BreadcrumbItem, BreadcrumbSeparator } from "./ui/breadcrumb"

import { AppSidebar } from "@/components/app-sidebar"
import type { BreadcrumbItemLink, LayoutType } from "@/types/general"
import { Link, useLocation } from "react-router"
import AuthContext from "@/contexts/AuthContext"
import type { AuthContextType } from "@/types/authorization"


export const Breadcrumbs = ({items}: {items: BreadcrumbItemLink[]}) => (
    items
        .map((item, index) => (
            <Fragment key={index}>
                {index ? <BreadcrumbSeparator className="hidden md:block" /> : null}
                <BreadcrumbItem >
                    <Link to={item.link}>{item.name}</Link>
                </BreadcrumbItem>
            </Fragment>
        ))
)

const Layout: LayoutType = ({ header, children, auxSidebar }) => {
    const [open, setOpen] = useState(true)
    const {setRedirect} = useContext(AuthContext) as AuthContextType
    // The page's own location, captured once: nested routes such as `<page>/settings`
    // must not overwrite it, because the settings dialog closes by navigating back to it.
    const [pageLocation] = useState(useLocation())

    useEffect(() => setRedirect(pageLocation), [pageLocation, setRedirect])
    
    return(
        <SidebarProvider open={open} onOpenChange={setOpen}>
            <AppSidebar />
            <SidebarInset>
                {header}
                {children}
            </SidebarInset>
            {auxSidebar}
        </SidebarProvider>
    )
}

export default Layout