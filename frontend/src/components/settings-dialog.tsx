"use client"

import {
  Link as LucideLink,
  Lock,
  Settings,
  CircleUser,
  Users,
  Building,
  Server,
  Database,
} from "lucide-react"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarProvider,
} from "@/components/ui/sidebar"
import { Link, useNavigate } from "react-router"
import { useContext, useState } from "react"
import AuthContext from "@/contexts/AuthContext"
import type { AuthContextType } from "@/types/authorization"

const data = {
  nav: [
    { name: "General", icon: Settings, url: "general" },
    { name: "Account", icon: CircleUser, url: "account" },
    { name: "Privacy & Visibility", icon: Lock, url: "privacy" },
    { name: "Affiliations", icon: LucideLink, url: "affiliations" },
    { name: "User Management", icon: Users, url: "users" },
    { name: "Locations", icon: Building, url: "locations" },
    { name: "Devices", icon: Server, url: "devices" },
    { name: "Databases", icon: Database, url: "databases" },
  ],
}

const SettingsPlaceholder = () => (
  <div className="flex flex-1 flex-col gap-4 overflow-y-auto p-4 pt-0">
    {Array.from({ length: 10 }).map((_, index) => (
        <div
        key={index}
        className="bg-muted/50 aspect-video max-w-3xl rounded-xl"
        />
    ))}
  </div>
)

export const SettingsDialog = () => {
  const navigate = useNavigate()
  const {redirect} = useContext(AuthContext) as AuthContextType

  // const [redirects, setRedirects] = useState<number>(-1)
  const [activeItem, setActiveItem] = useState(data.nav[0])

  return (
    <Dialog open onOpenChange={() => navigate(redirect ?? "/")}>
      <DialogContent
        className="overflow-hidden p-0 md:max-h-[500px] md:max-w-[700px] lg:max-w-[800px]"
      >
          <DialogTitle className="sr-only">Settings</DialogTitle>
          <DialogDescription className="sr-only">
          Customize your settings here.
          </DialogDescription>
          <SidebarProvider className="items-start">
            <Sidebar collapsible="none" className="hidden md:flex">
                <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupContent>
                    <SidebarMenu>
                        {data.nav.map((item) => (
                          <SidebarMenuItem key={item.name}>
                              <SidebarMenuButton
                                asChild
                                isActive={item.name === activeItem.name}
                              >
                              <Link
                                to={`#${item.url}`}
                                onClick={() => {
                                  // setRedirects(redirects-1) // hacky way of redirecting to first page
                                  setActiveItem(item)
                                }}>
                                  <item.icon />
                                  <span>{item.name}</span>
                              </Link>
                              </SidebarMenuButton>
                          </SidebarMenuItem>
                        ))}
                    </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
                </SidebarContent>
            </Sidebar>
            <main className="flex h-[480px] flex-1 flex-col overflow-hidden">
                <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
                <div className="flex items-center gap-2 px-4">
                    <Breadcrumb>
                    <BreadcrumbList>
                        <BreadcrumbItem className="hidden md:block">
                        <BreadcrumbLink href="#">Settings</BreadcrumbLink>
                        </BreadcrumbItem>
                        <BreadcrumbSeparator className="hidden md:block" />
                        <BreadcrumbItem>
                        <BreadcrumbPage>General</BreadcrumbPage>
                        </BreadcrumbItem>
                    </BreadcrumbList>
                    </Breadcrumb>
                </div>
                </header>
                <SettingsPlaceholder />
            </main>
            </SidebarProvider>
      </DialogContent>
    </Dialog>
  )
}
