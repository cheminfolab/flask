import {useEffect, useState} from "react";
import {Col, Container, Pagination, Row} from "react-bootstrap";
import ChemComTable from "../components/ChemComTable";
import ChemSidebarComp from "../components/ChemSidebarComp";
import useAxios from "../utils/useAxios";
// import ChemDetailComp from "../components/ChemDetailComp";
import {Compound, Substance} from "../@types/chemicals";
import ChemSubTable from "../components/ChemSubTable";
import {ChemSubNavbar} from "../components/ChemNavbars";


export const SubPage = () => {

    let ApiService = useAxios(true)
    let [substances, setSubstances] = useState<Substance[]>([])
    let [selected, setSelected] = useState<number[]>([])
    // let [containers, setContainers] = useState([])
    // let [containerDetail, setContainerDetail] = useState({
    //     id: null,
    //     substance: {image:null}
    // })
    // let [containerId, setContainerId] = useState()
    // let [show, setShow] = useState(false)

    useEffect(() => {
        ApiService
            .getAll('substance')
            .then(res => setSubstances(res))
            .catch(error => console.log('getAll error:', error))
    }, [])

    // useEffect(() => console.log(substances), [substances])

    // useEffect(() => {
    //     console.log('substanceId', substanceId)
    //     if (substanceId) {
    //     ApiService
    //         .get('substance', substanceId)
    //         .then(returnedsubstance => setsubstanceDetail(returnedsubstance))
    //         .catch(error => console.log('get error:', error))
    // }}, [substanceId])

    return (
        <Container fluid>
            <Row className="mb-2 mt-2">
                <Col xs={2}>
                    <h3>Substances</h3>
                </Col>
                <Col xs={10}>
                    <ChemSubNavbar
                        substances={substances}
                        selected={selected}
                        setSelected={setSelected}
                    />
                </Col>
            </Row>
            <Row xs="auto">
                <Col xs={2} id="sidebar-wrapper">
                    <ChemSidebarComp/>
                </Col>
                <Col  xs={10} id="page-content-wrapper">
                    <div className="overflow-auto">
                    <ChemSubTable
                        substances={substances}
                        selected={selected}
                        setSelected={setSelected}
                        // setShow={setShow}
                        // setSubstanceId={setSubstanceId}
                    />

                    </div>
                    {/*<ChemDetailComp*/}
                    {/*    show={show}*/}
                    {/*    setShow={setShow}*/}
                    {/*    substanceId={substanceId}*/}
                    {/*/>*/}
                </Col>
            </Row>
            <Row>
                <Col xs={2}/>
                <Col xs={9}>
                    <Pagination className="d-flex justify-content-center">
                      <Pagination.First />
                      <Pagination.Prev />
                      <Pagination.Item>{1}</Pagination.Item>
                      <Pagination.Ellipsis />

                      <Pagination.Item>{10}</Pagination.Item>
                      <Pagination.Item>{11}</Pagination.Item>
                      <Pagination.Item active>{12}</Pagination.Item>
                      <Pagination.Item>{13}</Pagination.Item>
                      <Pagination.Item disabled>{14}</Pagination.Item>

                      <Pagination.Ellipsis />
                      <Pagination.Item>{20}</Pagination.Item>
                      <Pagination.Next />
                      <Pagination.Last />
                    </Pagination>

                </Col>
            </Row>
        </Container>
    );
}

export const ComPage = () => {

    let ApiService = useAxios(true)
    let [compounds, setCompounds] = useState<Compound[]>([])
    // let [containers, setContainers] = useState([])
    // let [containerDetail, setContainerDetail] = useState({
    //     id: null,
    //     substance: {image:null}
    // })
    // let [containerId, setContainerId] = useState()
    // let [show, setShow] = useState(false)

    useEffect(() => {
        ApiService
            .getAll('compound')
            .then(res => setCompounds(res))
            .catch(error => console.log('getAll error:', error))
    }, [])

    // useEffect(() => console.log(compounds), [compounds])

    // useEffect(() => {
    //     console.log('compoundId', compoundId)
    //     if (compoundId) {
    //     ApiService
    //         .get('compound', compoundId)
    //         .then(returnedcompound => setcompoundDetail(returnedcompound))
    //         .catch(error => console.log('get error:', error))
    // }}, [compoundId])

    return (
        <Container fluid className="mb-2">
            <Row>
                <Col xs={2}>
                    <h3>Chemicals</h3>
                </Col>
                <Col xs={10}>
                    {/*<ChemComNavbar/>*/}
                </Col>
            </Row>
            <Row>
                <Col xs={2} id="sidebar-wrapper">
                    <ChemSidebarComp/>
                </Col>
                <Col  xs={10} id="page-content-wrapper">
                    <ChemComTable
                        compounds={compounds}
                        // setShow={setShow}
                        // setCompoundId={setCompoundId}
                    />

                    {/*<ChemDetailComp*/}
                    {/*    show={show}*/}
                    {/*    setShow={setShow}*/}
                    {/*    compoundId={compoundId}*/}
                    {/*/>*/}
                </Col>
            </Row>
        </Container>
    );
}