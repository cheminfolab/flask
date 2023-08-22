import {useEffect, useState} from "react";
import {Col, Container, Row} from "react-bootstrap";
import ChemTableComp from "../components/ChemTableComp";
import ChemSidebarComp from "../components/ChemSidebarComp";
import useAxios from "../utils/useAxios";
import ChemDetailComp from "../components/ChemDetailComp";


const ChemPage = () => {

    let ApiService = useAxios(true)
    let [containers, setContainers] = useState([])
    let [containerDetail, setContainerDetail] = useState({
        id: null,
        substance: {image:null}
    })
    let [containerId, setContainerId] = useState()
    let [show, setShow] = useState(false)

    useEffect(() => {
        ApiService
            .getAll('container')
            .then(returnedContainers => setContainers(returnedContainers))
            .catch(error => console.log('getAll error:', error))
    }, [])

    useEffect(() => console.log(containers), [containers])

    useEffect(() => {
        console.log('containerId', containerId)
        if (containerId) {
        ApiService
            .get('container', containerId)
            .then(returnedContainer => setContainerDetail(returnedContainer))
            .catch(error => console.log('get error:', error))
    }}, [containerId])

    return (
        <Container fluid>
            <Row>
                <Col xs={2} id="sidebar-wrapper">
                    <ChemSidebarComp/>
                </Col>
                <Col  xs={10} id="page-content-wrapper">
                    <ChemTableComp
                        compounds={containers}
                        setShow={setShow}
                        setCompoundId={setContainerId}
                    />
                    <ChemDetailComp
                        show={show}
                        setShow={setShow}
                        compoundId={containerId}
                    />
                </Col>
            </Row>
        </Container>
    );
}

export default ChemPage