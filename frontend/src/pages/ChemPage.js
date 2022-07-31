import {useContext, useEffect, useState} from "react";
import {Col, Container, Row} from "react-bootstrap";
import AuthContext from "../context/AuthContext";
import ChemTableComp from "../components/ChemTableComp";
import ChemSidebarComp from "../components/ChemSidebarComp";
import useAxios from "../utils/useAxios";
import ChemDetailComp from "../components/ChemDetailComp";

const ChemPage = () => {

    let {logoutUser} = useContext(AuthContext)
    let [compounds, setCompounds] = useState([])
    let [show, setShow] = useState(false)
    let api = useAxios(true)

    useEffect(() => {
        getCompounds();
    }, [])

    let getCompounds = async () => {
        await api.get('/compound/')
            .then( (response) => {
                if (response.status === 200){
                    setCompounds(response.data)
                } else if (response.statusText === 'Unauthorized'){
                    logoutUser()
                }
            })
            .catch( (error) => console.log(error))
    }

    return (
        <Container fluid>
            <ChemDetailComp show={show} setShow={setShow}/>
            <Row>
                <Col xs={2} id="sidebar-wrapper">
                    <ChemSidebarComp/>
                </Col>
                <Col  xs={10} id="page-content-wrapper">
                    <ChemTableComp compounds={compounds} setShow={setShow}/>
                </Col>
            </Row>
        </Container>
    );
}

export default ChemPage