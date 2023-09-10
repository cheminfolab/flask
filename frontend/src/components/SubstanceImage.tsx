import './SubstanceImage.css'
import {Image} from "react-bootstrap";

const SubstanceImage = ({path}) => <Image
    src={process.env.REACT_APP_API_BASE_URL+String(path)}
    alt={'chemical structure'}
    rounded
/>

export default SubstanceImage;