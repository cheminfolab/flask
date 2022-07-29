import {useContext, useEffect, useState} from "react";
import AuthContext from "../context/AuthContext";
import ChemTableComp from "../components/ChemTableComp";
import useAxios from "../utils/useAxios";

const ChemPage = () => {

    let {logoutUser} = useContext(AuthContext)
    let [compounds, setCompounds] = useState([])
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
        <div className='col-12'>
            <ChemTableComp compounds={compounds}/>
        </div>
    );
}

export default ChemPage