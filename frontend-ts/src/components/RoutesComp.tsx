import {Route, Routes} from "react-router-dom";
import PrivateRoute from "../utils/PrivateRoute";

import HomePage from "../pages/HomePage";
import AuthPage from "../pages/AuthPage";
import ChemPage from "../pages/ChemPage";
import ProjectPage from "../pages/ProjectPage";
import '../pages/AuthPage.css'

const RoutesComp = () => {
    return (
        <div>
            <Routes>
                <Route
                    path="/"
                    element={<PrivateRoute><HomePage/></PrivateRoute>}
                    exact
                />
                <Route
                    path="/login"
                    element={<AuthPage/>}
                />
                <Route
                    path="/chemicals"
                    element={<PrivateRoute><ChemPage/></PrivateRoute>}
                />
                <Route
                    path="/projects"
                    element={<PrivateRoute><ProjectPage/></PrivateRoute>}
                />
            </Routes>
        </div>
    );
}

export default RoutesComp;