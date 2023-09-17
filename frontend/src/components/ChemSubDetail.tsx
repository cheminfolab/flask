import {useState} from "react";
import {Col, Container, Form, Modal, Row, Tab, Table, Tabs} from "react-bootstrap";
import SubstanceImage from "./SubstanceImage";
import FormulaFormatter from "./FormulaFormatter";
import DataRow from "./DataRow";

const SubstanceDetail = ({units, substance, setDetail}) => {
    let [edit, setEdit] = useState(false)
    if (substance) return(
        <Modal
          show={substance !== null}
          onHide={() => setDetail(null)}
          dialogClassName="modal-90w"
          centered
        >
            <Modal.Header closeButton>
            <Modal.Title>
                {substance.name}
            </Modal.Title>
            </Modal.Header>
                <Modal.Body>
                            <Form>
                    <Container>
                        <Row>
                                {substance.image
                                    ? <Col xs={12} lg={2} className={"d-flex justify-content-center"}><SubstanceImage path={substance.image}/></Col>
                                    : null
                                }
                                <Col xs={12} lg={5}>
                                    <Table borderless>
                                        <tbody>
                                            <DataRow
                                                name={"formula"}
                                                data={substance.formula}
                                                edit={edit}
                                                text={<FormulaFormatter formula={substance.formula}/>}
                                            />
                                            <DataRow
                                                name={"CAS"}
                                                data={substance.cas}
                                                edit={edit}
                                            />
                                            <DataRow
                                                name={"PubChem SID"}
                                                data={substance.pubchem_sid}
                                                edit={edit}
                                            />
                                            <DataRow
                                                name={"PubChem CID"}
                                                data={substance.pubchem_cid}
                                                edit={edit}
                                            />
                                            <DataRow
                                                name={"InChI"}
                                                data={substance.inchi}
                                                edit={edit}
                                            />
                                            <DataRow
                                                name={"InChI key"}
                                                data={substance.inchi_key}
                                                edit={edit}
                                            />
                                            <DataRow
                                                name={"SMILES"}
                                                data={substance.smiles}
                                                edit={edit}
                                            />
                                        </tbody>
                                    </Table>
                                </Col>
                                <Col xs={12} lg={5}>
                                    <Table borderless>
                                        <tbody>
                                            <DataRow
                                                name={"name"}
                                                data={substance.name}
                                                edit={edit}
                                            />
                                            <DataRow
                                                name={"label"}
                                                data={substance.label}
                                                edit={edit}
                                            />
                                            <DataRow
                                                name={"synonyms"}
                                                data={substance.synonyms}
                                                edit={edit}
                                            />
                                        </tbody>
                                    </Table>
                                </Col>
                        </Row>
                    </Container>
                            </Form>
                <Tabs
                  defaultActiveKey="home"
                  transition={false}
                  className="mb-3"
                >
                  <Tab eventKey="home" title="Properties">
                    <Container>
                      <Row>
                          <Col lg={2}></Col>
                        <Col xs={12} lg={10}>
                            <Table borderless>
                                <tbody>
                                    <DataRow
                                        name={"molar mass"}
                                        data={substance.mol_weight}
                                        edit={edit}
                                        units={units}
                                        unit={substance.mol_weight_unit}
                                    />
                                    <DataRow
                                        name={"exact mass"}
                                        data={substance.exact_mass}
                                        edit={edit}
                                        units={units}
                                        unit={substance.exact_mass_unit}
                                    />
                                </tbody>
                            </Table>
                        </Col>
                      </Row>
                    </Container>
                  </Tab>
                  <Tab eventKey="structure" title="Structure">
                      <p>
                        Ipsum molestiae natus adipisci modi eligendi? Debitis amet quae unde
                        commodi aspernatur enim, consectetur. Cumque deleniti temporibus
                        ipsam atque a dolores quisquam quisquam adipisci possimus
                        laboriosam. Quibusdam facilis doloribus debitis! Sit quasi quod
                        accusamus eos quod. Ab quos consequuntur eaque quo rem! Mollitia
                        reiciendis porro quo magni incidunt dolore amet atque facilis ipsum
                        deleniti rem!
                      </p>
                  </Tab>
                  <Tab eventKey="analysis" title="Analysis">
                      <p>
                        Ipsum molestiae natus adipisci modi eligendi? Debitis amet quae unde
                        commodi aspernatur enim, consectetur. Cumque deleniti temporibus
                        ipsam atque a dolores quisquam quisquam adipisci possimus
                        laboriosam. Quibusdam facilis doloribus debitis! Sit quasi quod
                        accusamus eos quod. Ab quos consequuntur eaque quo rem! Mollitia
                        reiciendis porro quo magni incidunt dolore amet atque facilis ipsum
                        deleniti rem!
                      </p>
                  </Tab>
                  <Tab eventKey="related" title="Related">
                      <p>
                        Ipsum molestiae natus adipisci modi eligendi? Debitis amet quae unde
                        commodi aspernatur enim, consectetur. Cumque deleniti temporibus
                        ipsam atque a dolores quisquam quisquam adipisci possimus
                        laboriosam. Quibusdam facilis doloribus debitis! Sit quasi quod
                        accusamus eos quod. Ab quos consequuntur eaque quo rem! Mollitia
                        reiciendis porro quo magni incidunt dolore amet atque facilis ipsum
                        deleniti rem!
                      </p>
                  </Tab>
                </Tabs>
                {/*<Form>*/}
                {/*  <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">*/}
                {/*    <Form.Label>Email address</Form.Label>*/}
                {/*    <Form.Control*/}
                {/*      type="email"*/}
                {/*      name="email2"*/}
                {/*      placeholder="name@example.com"*/}
                {/*      autoFocus*/}
                {/*    />*/}
                {/*  </Form.Group>*/}
                {/*  <Form.Group*/}
                {/*      className="mb-3"*/}
                {/*      controlId="exampleForm.ControlTextarea1"*/}
                {/*  >*/}
                {/*    <Form.Label>Example textarea</Form.Label>*/}
                {/*    <Form.Control as="textarea" rows={3} />*/}
                {/*  </Form.Group>*/}
                {/*</Form>*/}
            </Modal.Body>
        </Modal>
    )
}

export default SubstanceDetail