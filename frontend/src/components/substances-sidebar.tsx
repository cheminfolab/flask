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
    SidebarSeparator
} from "./ui/sidebar"
import {
    Collapsible, 
    CollapsibleContent, 
    CollapsibleTrigger 
} from "./ui/collapsible"
import { ChevronRight } from "lucide-react"
import {
    MultiSelect, 
    MultiSelectContent, 
    MultiSelectGroup, 
    MultiSelectItem, 
    MultiSelectTrigger, 
    MultiSelectValue 
} from "./ui/multi-select"

const SubstanceSidebar = () => {

    // identifiers: CAS, InChI, InChIKey, names
    // properties: formula, molecular weight, physical properties etc.
    // tags

    const owners = [
        {id: "huber", name: "Huber"},
        {id: "merten", name: "Merten"},
        {id: "goossen", name: "Gooßen"},
        {id: "dyker", name: "Dyker"},
        {id: "gessner", name: "Däschlein-Gessner"}
    ]

    const locations = [
        {room: "NC 4/159", storages: [
            {name: "solvent cabinet"},
        ]}
    ]

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
                                                    {owners.map((owner, index) => (
                                                        <MultiSelectItem
                                                            key={index}
                                                            value={owner.id}
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
                                                {locations.map((location, locationIndex) => (
                                                    <MultiSelectGroup key={locationIndex}>
                                                        {location.storages.map((storage, storageIndex) => (
                                                            <MultiSelectItem
                                                                key={storageIndex}
                                                                value={storage.name}
                                                            >
                                                                {storage.name}
                                                            </MultiSelectItem>
                                                        ))}
                                                    </MultiSelectGroup>

                                                ))}
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

export default SubstanceSidebar