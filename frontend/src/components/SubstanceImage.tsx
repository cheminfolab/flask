import './SubstanceImage.css'
import {Image} from "react-bootstrap";

// todo: use env variable
const SubstanceImage = ({path}) => {
    return (
        <div>
            <Image src={'http://127.0.0.1:8000'+String(path)} alt={'chemical structure'} rounded />
        </div>
    );
}

export default SubstanceImage;