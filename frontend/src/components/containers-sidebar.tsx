import { 
    Sidebar, 
    SidebarContent, 
    SidebarFooter, 
    SidebarGroup, 
    SidebarGroupContent, 
    SidebarGroupLabel, 
    SidebarHeader, 
    SidebarMenu,
    SidebarMenuItem,
    SidebarSeparator,
} from "./ui/sidebar"
import {
    Collapsible, 
    CollapsibleContent, 
    CollapsibleTrigger,
} from "./ui/collapsible"
import { ChevronRight } from "lucide-react"
import { useEffect, useState } from "react"
import useAxios from "@/hooks/useAxios"
import type { Storage, WorkingGroup } from "@/types/api"
import {
    MultiSelect,
    MultiSelectContent,
    MultiSelectGroup,
    MultiSelectItem,
    MultiSelectTrigger,
    MultiSelectValue,
} from "./ui/multi-select"

const ContainerSidebar = () => {

    // identifiers: CAS, InChI, InChIKey, names
    // properties: formula, molecular weight, physical properties etc.
    // tags

    const api = useAxios()
    const [owners, setOwners] = useState<WorkingGroup[]>([])
    const [storages, setStorages] = useState<Storage[]>([])

    useEffect(() => {
        api.getAll<WorkingGroup[]>("groups").then(setOwners).catch(() => setOwners([]))
        api.getAll<Storage[]>("storages").then(setStorages).catch(() => setStorages([]))
    }, [api])

    return(
        <Sidebar collapsible="offcanvas" side="right">
            <SidebarHeader>
                Filters
            </SidebarHeader>
            <SidebarSeparator className="mx-0" />
            <SidebarContent>
                <SidebarGroup>
                    <Collapsible defaultOpen={true} className="group/collapsible">
                        <SidebarGroupLabel
                            asChild
                            className="group/label text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground w-full text-sm"
                        >
                            <CollapsibleTrigger>
                                Locations and Owners
                                <ChevronRight className="ml-auto transition-transform group-data-[state=open]/collapsible:rotate-90" />
                            </CollapsibleTrigger>
                        </SidebarGroupLabel>
                        <CollapsibleContent>
                            <SidebarGroupContent>
                                <SidebarMenu>
                                    <SidebarMenuItem>
                                        <MultiSelect>
                                            <MultiSelectTrigger className="w-full max-w-[400px]">
                                                <MultiSelectValue placeholder="Select owners..." />
                                            </MultiSelectTrigger>
                                            <MultiSelectContent>
                                                <MultiSelectGroup>
                                                    {owners.map(owner => (
                                                        <MultiSelectItem
                                                            key={owner.id}
                                                            value={String(owner.id)}
                                                        >
                                                            {owner.name}
                                                        </MultiSelectItem>
                                                    ))}
                                                </MultiSelectGroup>
                                            </MultiSelectContent>
                                        </MultiSelect>
                                    </SidebarMenuItem>
                                    <SidebarMenuItem>
                                        <MultiSelect>
                                            <MultiSelectTrigger className="w-full max-w-[400px]">
                                                <MultiSelectValue placeholder="Select locations..." />
                                            </MultiSelectTrigger>
                                            <MultiSelectContent>
                                                <MultiSelectGroup>
                                                    {storages.map(storage => (
                                                        <MultiSelectItem
                                                            key={storage.id}
                                                            value={String(storage.id)}
                                                        >
                                                            {storage.label}
                                                        </MultiSelectItem>
                                                    ))}
                                                </MultiSelectGroup>
                                            </MultiSelectContent>
                                        </MultiSelect>
                                    </SidebarMenuItem>
                                </SidebarMenu>
                            </SidebarGroupContent>
                        </CollapsibleContent>
                    </Collapsible>
                </SidebarGroup>
            <SidebarSeparator className="mx-0" />
            </SidebarContent>
            <SidebarFooter />
        </Sidebar>
    )
}

export default ContainerSidebar