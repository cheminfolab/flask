import {
    Card, Col,
    Container,
    Dropdown,
    DropdownButton, Form,
    Nav,
    Navbar,
    NavDropdown, Row
} from "react-bootstrap";
import {Link} from "react-router-dom";

export const ChemSubNavbar = ({substances, selected, setSelected}) => {
    const checkAll = () => {
        selected.length === substances.length
            ? setSelected([])
            : setSelected(substances.map(substance => substance.id))
    }
    return (
        <Card>
            <Card.Header>
                <Row className={"align-items-center"}>
                    <Col xs={1} >
                        <Nav className="me-auto">
                            <Form>
                                <Form.Check
                                    type="checkbox"
                                    id="select-all"
                                    label="all"
                                    onChange={checkAll}
                                    checked={selected.length === substances.length}
                                />
                            </Form>
                        </Nav>
                    </Col>
                    <Col xs={4}>
                        <Nav className="me-auto d-flex justify-content-center">
                            <NavDropdown title={<i className="bi bi-plus-square"/>} id="basic-nav-dropdown">
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-sticky"/> empty
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-subtract"/> copy from existent
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-upc-scan"/> from UPC
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-qr-code"/> from QR
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-database-add"></i> from database
                                </NavDropdown.Item>
                            </NavDropdown>
                            <Nav.Link as={Link} to={"#"} disabled={selected.length !== 1}>
                                <i className="bi bi-pencil-square"/>
                            </Nav.Link>
                            <Nav.Link as={Link} to={"#"} disabled={selected.length === 0}>
                                <i className="bi bi-tag"/>
                            </Nav.Link>
                            <Nav.Link as={Link} to={"#"} disabled={selected.length === 0}>
                                <i className="bi bi-trash"/>
                            </Nav.Link>
                            {/* edit mode: */}
                            {/*<Nav.Link as={Link} to={"#"}><i className="bi bi-arrow-left-square"/></Nav.Link>*/}
                            {/*<Nav.Link as={Link} to={"#"}><i className="bi bi-arrow-right-square"/></Nav.Link>*/}
                        </Nav>
                    </Col>
                    <Col xs={3}>
                        <Nav className="d-flex justify-content-center">
                            <Nav.Link as={Link} to={"#"} disabled={selected.length === 0}>
                                <i className="bi bi-share"/>
                            </Nav.Link>
                            <Nav.Link as={Link} to={"#"} disabled={selected.length === 0}>
                                <i className="bi bi-database"/>
                            </Nav.Link>
                            <Nav.Link as={Link} to={"#"} disabled={selected.length !== 1}>
                                <i className="bi bi-cart3"/>
                            </Nav.Link>
                            {/*<Nav.Link as={Link} to={"#"}><i className="bi bi-bag-check"/></Nav.Link>*/}
                            {/*<Nav.Link as={Link} to={"#"}><i className="bi bi-bag-plus"/></Nav.Link>*/}
                        </Nav>
                    </Col>
                    <Col xs={3}>
                        <Nav className="me-auto d-flex justify-content-center">
                            <NavDropdown title={<i className="bi bi-arrow-down-up"/>} id="basic-nav-dropdown">
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-save"/> save
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-plus-square-dotted"/> upload
                                </NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown title={<i className="bi bi-file-earmark-arrow-down"/>} id="basic-nav-dropdown">
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-file-earmark-pdf"/> pdf</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-file-earmark-word"/> Word
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-file-earmark-code"/> LaTeX
                                </NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.4">
                                    <i className="bi bi-file-earmark-spreadsheet"/> csv
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-file-earmark-code"/> JSON
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-file-earmark-code"/> SQL
                                </NavDropdown.Item>
                                <NavDropdown.Divider/>
                                <NavDropdown.Item href="#action/3.4"><i
                                    className="bi bi-file-earmark-zip"/> zip</NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown title={<i className="bi bi-sliders"/>} id="basic-nav-dropdown">
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <Row>
                                        <Col className="d-flex justify-content-left">
                                            <i className="bi bi-sort-down"/> sort
                                        </Col>
                                        <Col className="d-flex justify-content-right">
                                            <i className="bi bi-chevron-right"/>
                                        </Col>
                                    </Row>
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-list-ul"/> list
                                </NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}>
                                    <i className="bi bi-grid"/> grid
                                </NavDropdown.Item>
                            </NavDropdown>
                        </Nav>
                    </Col>
                    <Col xs={1}>
                        <Nav className="me-auto d-flex justify-content-right">
                            {/*<Nav.Link as={Link} to={"#"}><i className="bi bi-three-dots"/></Nav.Link>*/}
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-question-square"/></Nav.Link>
                        </Nav>
                    </Col>
                </Row>
            </Card.Header>
        </Card>
    )
}

export const ChemComNavbar = ({substances, selected, setSelected}) => {
    const checkAll = () => {
        selected.length === substances.length
            ? setSelected([])
            : setSelected(substances.map(substance => substance.id))
    }
    return (
        <Card>
            <Card.Header>
                <Row>
                    <Col xs={1} style={{float: 'left'}}>
                        <Nav className="me-auto">
                            <Form>
                                <Form.Check
                                    type="checkbox"
                                    id="select-all"
                                    label="all"
                                    onChange={checkAll}
                                    checked={selected.length === substances.length}
                                />
                            </Form>
                        </Nav>
                    </Col>
                    <Col xs={11}>
                        <Nav className="me-auto">
                            <NavDropdown title={<i className="bi bi-plus-square"/>} id="basic-nav-dropdown">
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-sticky"/> empty</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i className="bi bi-subtract"/> copy from existent</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i className="bi bi-upc-scan"/> from
                                    UPC</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i className="bi bi-qr-code"/> from
                                    QR</NavDropdown.Item>
                            </NavDropdown>
                            <Nav.Link as={Link} to={"#"} disabled={selected.length !== 1}><i className="bi bi-pencil-square"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"} disabled={selected.length === 0}><i className="bi bi-trash"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-question-square"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-tags"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-archive"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-arrow-left-square"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-arrow-right-square"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-share"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-database"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-cart3"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-bag-check"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-bag-plus"/></Nav.Link>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-quote"/></Nav.Link>
                            <NavDropdown title={<i className="bi bi-sliders"/>} id="basic-nav-dropdown">
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-sort-down"/> sort</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-list-ul"/> list</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i className="bi bi-list"/> list</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.4"><i className="bi bi-file-earmark-spreadsheet"/> csv</NavDropdown.Item>
                                <NavDropdown.Divider/>
                                <NavDropdown.Item href="#action/3.4"><i
                                    className="bi bi-file-earmark-zip"/> zip</NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown title={<i className="bi bi-arrow-down-up"/>} id="basic-nav-dropdown">
                                <NavDropdown.Item as={Link} to={"#"}><i className="bi bi-save"/> save</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-box-arrow-in-down"/> save</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-box-arrow-down"/></NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-box-arrow-in-up"/></NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-cloud-download"/></NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i className="bi bi-download"/></NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown title={<i className="bi bi-file-earmark-arrow-down"/>} id="basic-nav-dropdown">
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-file-earmark-pdf"/> pdf</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-file-earmark-word"/> Word</NavDropdown.Item>
                                <NavDropdown.Item as={Link} to={"#"}><i
                                    className="bi bi-file-earmark-code"/> LaTeX</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.4"><i className="bi bi-file-earmark-spreadsheet"/> csv</NavDropdown.Item>
                                <NavDropdown.Divider/>
                                <NavDropdown.Item href="#action/3.4"><i
                                    className="bi bi-file-earmark-zip"/> zip</NavDropdown.Item>
                            </NavDropdown>
                            <Nav.Link as={Link} to={"#"}><i className="bi bi-three-dots"/></Nav.Link>
                        </Nav>
                    </Col>
                </Row>
            </Card.Header>
        </Card>
    )
}
