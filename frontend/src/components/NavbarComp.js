import React, {useContext} from 'react';
import {
    Container,
    Navbar,
    Nav,
    NavDropdown,
    Form,
    FormControl,
    Button,
    DropdownButton,
    Dropdown
} from 'react-bootstrap';
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
                    <Nav.Link as={Link} to={"/"}>Wiki</Nav.Link>
                  </Nav>
                  <Form className="d-flex mx-auto">
                    <FormControl
                      type="search"
                      placeholder="Search (inactive)"
                      className="me-2"
                      aria-label="Search"
                    />
                    <Button variant="outline-success" disabled>Search</Button>
                  </Form>
                  <Nav className="mr-auto">
                      <DropdownButton
                        id={`dropdown-variants-secondary`}
                        variant={'secondary'}
                        title={<i className="bi bi-gear"></i>}
                      >
                        <Dropdown.Item eventKey="1">Account</Dropdown.Item>
                        <Dropdown.Item eventKey="2">Another action</Dropdown.Item>

                        <Dropdown.Divider />

                        {user ? (
                            <Dropdown.Item onClick={logoutUser}>Logout</Dropdown.Item>
                        ):(
                            <Dropdown.Item as={Link} to={"/login"}>Login</Dropdown.Item>
                        )}
                      </DropdownButton>
                  </Nav>
                </Navbar.Collapse>
              </Container>
            </Navbar>
        </div>
    );
}

export default NavbarComp;