import {useState} from "react";
import {Col, Row, Table, Card, Button, Form, Modal, Container, Tabs, Tab} from "react-bootstrap";
import SubstanceImage from "./SubstanceImage";
import FormulaFormatter from "./FormulaFormatter";
import "./ChemSubTable.css"
import {Substance} from "../@types/chemicals";
import SubstanceDetail from "./ChemSubDetail";
import DataRow from "./DataRow";

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
                    <Col
                        xs={11}
                        className="fs-5 text-lg-start text-wrap"
                        onClick={() => setDetail(substance)}
                        style={{cursor: 'pointer'}}
                    >
                        <span>{substance.name} {substance.label ? <span>({substance.label})</span> : null}</span>
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
                    <Col xs={5}>
                        <Table borderless>
                            <tbody>
                                <DataRow
                                    name={"CAS"}
                                    data={substance.cas}
                                    edit={false}
                                />
                                <DataRow
                                    name={"formula"}
                                    data={substance.formula}
                                    text={<FormulaFormatter formula={substance.formula}/>}
                                    edit={false}
                                />
                                <DataRow
                                    name={"molar mass"}
                                    data={substance.mol_weight}
                                    units={units}
                                    unit={substance.mol_weight_unit}
                                    edit={false}
                                />
                            </tbody>
                        </Table>
                    </Col>
                    <Col xs={5}>
                        <Table borderless>
                            <tbody>
                                <DataRow
                                    name={"synonyms"}
                                    data={substance.synonyms}
                                    edit={false}
                                />
                            </tbody>
                        </Table>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
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