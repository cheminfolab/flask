import React from "react";
import {BrowserRouter as Router} from "react-router-dom";

import NavbarComp from "./components/NavbarComp";
import RoutesComp from "./components/RoutesComp";

import {AuthProvider} from "./context/AuthContext";
import './App.css';
import "bootstrap-icons/font/bootstrap-icons.css"


function App() {
  return (
    <div className="App">
        <Router>
            <AuthProvider>
                <NavbarComp/>
                <RoutesComp/>
            </AuthProvider>
        </Router>
    </div>
  );
}

export default App;
