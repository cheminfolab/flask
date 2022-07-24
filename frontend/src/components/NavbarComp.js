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


const NavbarComp = () => {

    let {user, logoutUser} = useContext(AuthContext);

    return (
        <div>
            <Navbar bg="light" expand="lg">
              <Container>
                <Navbar.Brand as={Link} to={"/home"}>Notebook</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                  <Nav className="me-auto">
                    <Nav.Link as={Link} to={"/reaction"}>Reaction</Nav.Link>
                    <NavDropdown title="Inventory" id="basic-nav-dropdown">
                        <NavDropdown.Item as={Link} to={"/chemicals"}>Chemicals</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to={"/#"}>Equipment</NavDropdown.Item>
                        <NavDropdown.Item as={Link} to={"/#"}>Something</NavDropdown.Item>

                        <NavDropdown.Divider />

                        <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
                    </NavDropdown>
                    <Nav.Link as={Link} to={"/"}>Equipment</Nav.Link>
                  </Nav>
                  <Form className="d-flex mx-auto">
                    <FormControl
                      type="search"
                      placeholder="Search"
                      className="me-2"
                      aria-label="Search"
                    />
                    <Button variant="outline-success">Search</Button>
                  </Form>
                  <Nav className="mr-auto">
                      <DropdownButton
                        id={`dropdown-variants-secondary`}
                        variant={'secondary'}
                        title={'Settings'}
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