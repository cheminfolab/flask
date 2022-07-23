import React, {useContext} from 'react';
import { Container, Navbar, Nav, NavDropdown, Form, FormControl, Button } from 'react-bootstrap';
import { Link } from "react-router-dom";

import AuthContext from "../context/AuthContext";
import Logo from "../flask.png";


const NavbarComp = () => {

    let {user, logoutUser} = useContext(AuthContext);

    return (
        <div>
            <Navbar bg="light" expand="lg">
              <Container>
                <Navbar.Brand as={Link} to={"/"}>
                    <img
                      alt="Flask logo"
                      src={Logo}
                      width="30"
                      height="30"
                      className="d-inline-block align-top"
                    />{' '}
                    FLASK
                </Navbar.Brand>
                {/*<a href="https://www.flaticon.com/free-icons/experimentation" title="experimentation icons">Experimentation icons created by Freepik - Flaticon</a>*/}
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                  <Nav className="me-auto">
                    <Nav.Link as={Link} to={"/projects"}>Projects</Nav.Link>
                    <NavDropdown title="Inventory" id="basic-nav-dropdown">
                        <NavDropdown.Item as={Link} to={"/chemicals"}>Chemicals</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to={"/#"}>Equipment</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to={"/#"}>Something</NavDropdown.Item>
                        <NavDropdown.Divider />
                        <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
                    </NavDropdown>
                    <Nav.Link as={Link} to={"/"}>Equipment</Nav.Link>
                    {user ? (
                        <Nav.Link onClick={logoutUser}>Logout</Nav.Link>
                    ):(
                        <Nav.Link as={Link} to={"/login"}>Login</Nav.Link>
                    )}
                  </Nav>
                  <Form className="d-flex">
                    <FormControl
                      type="search"
                      placeholder="Search"
                      className="me-2"
                      aria-label="Search"
                    />
                    <Button variant="outline-success">Search</Button>
                  </Form>
                </Navbar.Collapse>
              </Container>
            </Navbar>
        </div>
    );
}

export default NavbarComp;