import { useContext, type ReactNode } from "react"
import {
    Navigate, 
    Route, 
    Routes
} from "react-router"
import Home from "@/pages/home"
import Substances from "@/pages/substances"
import Login from "@/pages/login"
import Signup from "@/pages/signup"
import { SettingsDialog } from "@/components/settings-dialog"
import AuthContext from "@/contexts/AuthContext"
import type { AuthContextType } from "@/types/authorization"

// TODO: use layout routes

const PrivateRoute = ({children}: {children: ReactNode}) => {
    const {user} = useContext(AuthContext) as AuthContextType
    return user ? children : <Navigate to="/login" />
}

type RoutingType = () => ReactNode

const Routing: RoutingType = () => (
    <Routes>
        <Route path="/" element={<PrivateRoute><Home/></PrivateRoute>}>
            <Route path="settings" element={<SettingsDialog/>}/>
        </Route>
        <Route path="login" element={<Login/>}/>
        <Route path="signup" element={<Signup/>}/>
        <Route path="substances" element={<PrivateRoute><Substances/></PrivateRoute>}>
            <Route path="settings" element={<SettingsDialog/>}/>
        </Route>
    </Routes>
)
export default Routing