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
    let [compoundDetail, setCompoundDetail] = useState([])
    let [compoundId, setCompoundId] = useState(1)
    let [show, setShow] = useState(false)
    let api = useAxios(true)

    useEffect(() => {
        getCompounds();
    }, [])

    let getapi = async (url, setState) => {
        await api.get(url)
            .then( (response) => {
                if (response.status === 200){
                    setState(response.data)
                } else if (response.statusText === 'Unauthorized'){
                    logoutUser()
                }
            })
            .catch( (error) => console.log(error))
    }

    let getCompounds = () => getapi('/compound/', setCompounds)
    let getCompoundDetail = id => getapi(`/compound/${id}`, setCompoundDetail)

    useEffect(() => {
        if (compoundId){
            getCompoundDetail(compoundId)
        }
        return
    }, [compoundId])

    return (
        <Container fluid>
            <Row>
                <Col xs={2} id="sidebar-wrapper">
                    <ChemSidebarComp/>
                </Col>
                <Col  xs={10} id="page-content-wrapper">
                    <ChemTableComp
                        compounds={compounds}
                        setShow={setShow}
                        setCompoundId={setCompoundId}
                    />
                    <ChemDetailComp
                        show={show}
                        setShow={setShow}
                        compoundDetail={compoundDetail}
                    />
                </Col>
            </Row>
        </Container>
    );
}

export default ChemPage