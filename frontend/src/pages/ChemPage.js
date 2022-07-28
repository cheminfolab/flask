import {useContext, useEffect, useState} from "react";
import AuthContext from "../context/AuthContext";
import ChemTableComp from "../components/ChemTableComp";
import ChemSidebarComp from "../components/ChemSidebarComp";
import {Col, Container, Row} from "react-bootstrap";

const ChemPage = () => {

    let {authTokens, logoutUser} = useContext(AuthContext)
    let [compounds, setCompounds] = useState([])

    useEffect(() => {
        getCompounds();
    }, [])

    let getApiResponse = async (items, setState) => {
        let response = await fetch('http://127.0.0.1:8000/api/'+String(items), {
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization':'Bearer ' + String(authTokens.access)
            }
        })
        let data = await response.json()
        if(response.status === 200){
            setState(data)
        }else if(response.statusText === 'Unauthorized'){
            logoutUser()
        }
    }

    let getCompounds = () => getApiResponse('compounds', setCompounds)

    return (
        <Container fluid>
            <Row>
                <Col xs={2} id="sidebar-wrapper">
                    <ChemSidebarComp/>
                </Col>
                <Col  xs={10} id="page-content-wrapper">
                    <ChemTableComp compounds={compounds}/>
                </Col>
            </Row>
        </Container>
    );
}

export default ChemPage