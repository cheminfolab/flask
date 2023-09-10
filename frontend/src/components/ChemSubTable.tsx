import {Col, Row, Table, Card, Button, Form} from "react-bootstrap";
import SubstanceImage from "./SubstanceImage";
import "./ChemComTable.css"
import FormulaFormatter from "./FormulaFormatter";

const SubstanceCard = ({substance, selected, setSelected}) => {
    const setSelection = () => {
        selected.includes(substance.id)
            ? setSelected(selected.filter(item => item !== substance.id))
            : setSelected([substance.id, ...selected])
    }
    return (
        <Card key={substance.id} className="mb-2">
            <Card.Header>
                <Row>
                    <Col xs={1}>
                        <Form style={{float: 'left'}}>
                            <Form.Check
                                checked={selected.includes(substance.id)}
                                onChange={setSelection}
                            />
                        </Form>
                    </Col>
                    <Col xs={10} className="fs-5 text-lg-start text-wrap">
                        {substance.name} {substance.cas ? <span>({substance.cas})</span> : null}
                    </Col>
                    <Col xs={1}>
                        {/*<Button variant="outline-secondary" style={{float: 'right'}}>edit</Button>*/}
                    </Col>
                </Row>
            </Card.Header>
            <Card.Body>
                <Row>
                    <Col xs={2}>
                        {substance.image ? <SubstanceImage path={substance.image}/> : null}
                    </Col>
                    <Col xs={2} className="text-lg-start">
                        <div>
                            <b>synonyms:</b><br/>
                            {substance.synonyms.map((syn, index) => <span key={index}>{syn}<br/></span>)}
                        </div>
                    </Col>
                    <Col xs={4}>
                        <Table borderless align={"left"}>
                            <tbody>
                                <tr>
                                    <td><b>formula:</b></td>
                                    <td><FormulaFormatter formula={substance.formula}/></td>
                                </tr>
                                <tr>
                                    <td><b>molar mass:</b></td>
                                    <td>{substance.mol_weight} {substance.mol_weight_unit}</td>
                                </tr>
                                <tr>
                                    <td><b>InChI:</b></td>
                                    <td>{substance.inchi}</td>
                                </tr>
                                <tr>
                                    <td><b>SMILES:</b></td>
                                    <td>{substance.smiles}</td>
                                </tr>
                            </tbody>
                        </Table>
                    </Col>
                    <Col xs={4}>
                        Acronym(s), label<br/>
                        Structures (3D)<br/>
                        Databases<br/>
                        (related structures)
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    )
}

const ChemSubTable = ({substances, selected, setSelected}) => {
    if (substances.length === 0) return(<Row>No data available.</Row>)
    return(substances.map(substance => (
        <SubstanceCard
            key={substance.id}
            substance={substance}
            selected={selected}
            setSelected={setSelected}
        />
    )))
}

export default ChemSubTable