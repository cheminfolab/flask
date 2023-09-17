import {useState} from "react";
import {Col, Row, Table, Card, Button, Form, Modal, Container, Tabs, Tab} from "react-bootstrap";
import SubstanceImage from "./SubstanceImage";
import FormulaFormatter from "./FormulaFormatter";
import "./ChemSubTable.css"
import {Substance} from "../@types/chemicals";

const DataRow = ({name, data, text=null}) => <tr>
    <td className={"py-0"}><b>{name}:</b></td>
    <td className={"py-0"} onClick={() => {navigator.clipboard.writeText(data)}}>{text? text : data}</td>
</tr>

const SubstanceCard = ({units, substance, selected, setSelected, setDetail}) => {
    const setSelection = () => {
        selected.includes(substance.id)
            ? setSelected(selected.filter(item => item !== substance.id))
            : setSelected([substance.id, ...selected])
    }
    return (
        <Card key={substance.id} className="mb-2">
            <Card.Header>
                <Row className={"align-items-center"}>
                    <Col xs={1}>
                        <Form style={{float: 'left'}}>
                            <Form.Check
                                checked={selected.includes(substance.id)}
                                onChange={setSelection}
                            />
                        </Form>
                    </Col>
                    <Col xs={11} className="fs-5 text-lg-start text-wrap">
                        <span onClick={() => setDetail(substance)}>{substance.name} {substance.label ? <span>({substance.label})</span> : null}</span>
                    </Col>
                </Row>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col xs={2} className={"position-relative"}>
                        {substance.image
                            ? <SubstanceImage
                                className={"position-absolute top-50 start-50 translate-middle"}
                                path={substance.image}
                                onClick={() => setDetail(substance)}
                              />
                            : null}
                    </Col>
                    <Col xs={4}>
                        <Table borderless>
                            <tbody>
                                <DataRow
                                    name={"CAS"}
                                    data={substance.cas}
                                />
                                <DataRow
                                    name={"formula"}
                                    data={substance.formula}
                                    text={<FormulaFormatter formula={substance.formula}/>}
                                />
                                <DataRow
                                    name={"molar mass"}
                                    data={substance.mol_weight}
                                    text={`${substance.mol_weight} ${
                                        units.find(u => u.id === substance.mol_weight_unit).symbol
                                    }`}
                                />
                            </tbody>
                        </Table>
                    </Col>
                    <Col xs={4}>
                        Acronym(s), label<br/>
                        Structures (3D)<br/>
                        Databases<br/>
                        (related structures)
                    </Col>
                    <Col xs={2} className="text-lg-start">
                        <div>
                            <b>synonyms:</b><br/>
                            {substance.synonyms.length
                                ? substance.synonyms.map((syn, index) => <span key={index}>{syn}<br/></span>)
                                : <span>-</span>}
                        </div>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

const SubstanceDetail = ({units, substance, setDetail}) => {
    // let [edit, setEdit] = useState(false)
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
            <Container>
              <Row>
                {substance.image
                    ? <Col xs={12} lg={2} className={"d-flex justify-content-center"}><SubstanceImage path={substance.image}/></Col>
                    : null
                }
                <Col xs={12} lg={10}>
                    <Table borderless>
                        <tbody>
                            <DataRow
                                name={"formula"}
                                data={substance.formula}
                                text={<FormulaFormatter formula={substance.formula}/>}
                            />
                            <DataRow
                                name={"CAS"}
                                data={substance.cas}
                            />
                            <DataRow
                                name={"PubChem SID"}
                                data={substance.pubchem_sid}
                            />
                            <DataRow
                                name={"PubChem CID"}
                                data={substance.pubchem_cid}
                            />
                            <DataRow
                                name={"InChI"}
                                data={substance.inchi}
                            />
                            <DataRow
                                name={"InChI key"}
                                data={substance.inchi_key}
                            />
                            <DataRow
                                name={"SMILES"}
                                data={substance.smiles}
                            />
                        </tbody>
                    </Table>
                </Col>
              </Row>
            </Container>
            <Tabs
              defaultActiveKey="home"
              transition={false}
              className="mb-3"
            >
              <Tab eventKey="home" title="Properties">
                <Container>
                  <Row>
                    <Col xs={12} lg={10}>
                        <Table borderless>
                            <tbody>
                                <DataRow
                                    name={"molar mass"}
                                    data={substance.mol_weight}
                                    text={`${substance.mol_weight} ${
                                        units.find(u => u.id === substance.mol_weight_unit).symbol
                                    }`}
                                />
                                <DataRow
                                    name={"exact mass"}
                                    data={substance.exact_mass}
                                    text={`${substance.exact_mass} ${
                                        units.find(u => u.id === substance.exact_mass_unit).symbol
                                    }`}
                                />
                            </tbody>
                        </Table>
                    </Col>
                  </Row>
                </Container>
              </Tab>
              <Tab eventKey="profile" title="Spectra">
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
              <Tab eventKey="contact" title="SDS">
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

const ChemSubTable = ({units, substances, selected, setSelected}) => {
    let [detail, setDetail] = useState<Substance | null>(null)
    if (substances.length === 0) return(<Row>No data available.</Row>)
    return(
        <>
            {substances.map(substance => (
                <SubstanceCard
                    units={units}
                    key={substance.id}
                    substance={substance}
                    selected={selected}
                    setSelected={setSelected}
                    setDetail={setDetail}
                />))}
            <SubstanceDetail
                units={units}
                substance={detail}
                setDetail={setDetail}
            />
        </>
    )
}

export default ChemSubTable