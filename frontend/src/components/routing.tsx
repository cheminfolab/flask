import {
    useContext,
    type ReactNode,
} from "react"
import {
    Navigate, 
    Route, 
    Routes,
} from "react-router"
import Home from "@/pages/home"
import Substances from "@/pages/substances"
import Login from "@/pages/login"
import Signup from "@/pages/signup"
import { SettingsDialog } from "@/components/settings-dialog"
import AuthContext from "@/contexts/AuthContext"
import type { AuthContextType } from "@/types/authorization"
import Projects from "@/pages/projects"
import Containers from "@/pages/containers"


type RoutingType = () => ReactNode
type PrivateRouteType = ({children}: {children: ReactNode}) => ReactNode

// TODO: use layout routes

const PrivateRoute: PrivateRouteType = ({children}) => {
    const {user} = useContext(AuthContext) as AuthContextType
    return user ? children : <Navigate to="/login" />
}

const Routing: RoutingType = () => {
    return(
        <Routes>
            <Route path="/" element={<PrivateRoute><Home/></PrivateRoute>}>
                <Route path="settings" element={<SettingsDialog/>}/>
            </Route>
            <Route path="home" element={<PrivateRoute><Navigate to="/" replace /></PrivateRoute>}>
                <Route path="settings" element={<SettingsDialog/>}/>
            </Route>
            <Route path="substances" element={<PrivateRoute><Substances/></PrivateRoute>}>
                <Route path="settings" element={<SettingsDialog/>}/>
            </Route>
            <Route path="containers" element={<PrivateRoute><Containers/></PrivateRoute>}>
                <Route path="settings" element={<SettingsDialog/>}/>
            </Route>
            <Route path="projects" element={<PrivateRoute><Projects/></PrivateRoute>}>
                <Route path="settings" element={<SettingsDialog/>}/>
            </Route>
            <Route path="login" element={<Login/>}/>
            <Route path="signup" element={<Signup/>}/>
        </Routes>
    )
}
export default Routing
