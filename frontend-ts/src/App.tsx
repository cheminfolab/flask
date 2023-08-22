import {BrowserRouter as Router} from "react-router-dom";
import NavbarComp from "./components/NavbarComp";
import RoutesComp from "./components/RoutesComp";

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import "bootstrap-icons/font/bootstrap-icons.css"

function App() {
  return (
    <div className="App">
      <Router>
        {/*<AuthProvider>*/}
            <NavbarComp/>
            <RoutesComp/>
        {/*</AuthProvider>*/}
      </Router>
    </div>
  );
}

export default App;
