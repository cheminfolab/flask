import {useEffect, useState} from "react";
import {Col, Container, Row} from "react-bootstrap";
import ChemTableComp from "../components/ChemTableComp";
import ChemSidebarComp from "../components/ChemSidebarComp";
import useAxios from "../utils/useAxios";
import ChemDetailComp from "../components/ChemDetailComp";
import {Compound} from "../@types/chemicals";


const ChemPage = () => {

    let ApiService = useAxios(true)
    let [compounds, setCompounds] = useState<Compound[]>([])
    // let [containers, setContainers] = useState([])
    // let [containerDetail, setContainerDetail] = useState({
    //     id: null,
    //     substance: {image:null}
    // })
    // let [containerId, setContainerId] = useState()
    let [show, setShow] = useState(false)

    useEffect(() => {
        ApiService
            .getAll('compound')
            .then(res => setCompounds(res))
            .catch(error => console.log('getAll error:', error))
    }, [])

    useEffect(() => console.log(compounds), [compounds])

    // useEffect(() => {
    //     console.log('compoundId', compoundId)
    //     if (compoundId) {
    //     ApiService
    //         .get('compound', compoundId)
    //         .then(returnedcompound => setcompoundDetail(returnedcompound))
    //         .catch(error => console.log('get error:', error))
    // }}, [compoundId])

    return (
        <Container fluid>
            <Row>
                <Col xs={2} id="sidebar-wrapper">
                    <ChemSidebarComp/>
                </Col>
                <Col  xs={10} id="page-content-wrapper">
                    <ChemTableComp
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

export default ChemPage