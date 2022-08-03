import {Table} from "react-bootstrap";
import SubstanceImage from "./SubstanceImage";

const ChemTableComp = ({compounds, setShow, getCompoundDetail}) => {

    const displayUnit = unitItem => String(unitItem.prefix)+String(unitItem.si)

    return(
        <Table striped bordered hover>
            <thead>
                <tr>
                    <th>Structure</th>
                    <th>Name</th>
                    <th>Formula</th>
                    <th>Molecular weight</th>
                    <th>Amount</th>
                    <th>Supplier</th>
                    <th>Purity</th>
                    <th>Density</th>
                    <th>Containment</th>
                    <th>Tara (incl. cap)</th>
                    <th>Price</th>
                    <th>Annotation</th>
                    <th>Location</th>
                    <th>Owner</th>
                    <th>Opened</th>
                </tr>
            </thead>
            <tbody>
                {compounds.map(
                    ({
                        id, density_unit, currency, owner, pubchem_cid, density, purity, opened, price, annotation,
                        last_used, last_user, created,
                        substance: {
                            mol_weight_unit, names, molecule, formula, smiles, inchi, inchi_key, cas, pubchem_sid,
                            mol_weight, exact_mass, color, melting_point, boiling_point, flash_point, image,
                            exact_mass_unit, melting_point_unit, boiling_point_unit, flash_point_unit
                        },
                        container: {
                            amount_unit, tara_unit,
                            location: {
                                name, compartment, room
                            },
                            supplier, EAN, product_number, amount, amount_left, tara, description
                        }
                    }) => (
                    <tr key={id} onClick={() => {
                        getCompoundDetail(id)
                        setShow(true)
                    }}>
                        <td>{(image ? <SubstanceImage path={image}/>: null)}</td>
                        <td>{names}</td>
                        <td>{formula}</td>
                        <td>{mol_weight} {displayUnit(mol_weight_unit)}</td>
                        <td>{amount_left}/{amount} {displayUnit(amount_unit)}</td>
                        {/* todo: add colored bar */}
                        <td>{supplier}</td>
                        <td>{purity}%</td>
                        <td>{density} {displayUnit(density_unit)}</td>
                        <td>{description}</td>
                        <td>{tara} {displayUnit(tara_unit)}</td>
                        <td>{price} {currency.currency}</td>
                        <td>{annotation}</td>
                        <td>R{room} {name} ({compartment})</td>
                        <td>{owner.name}</td>
                        <td>{opened}</td>
                    </tr>
                ))}
            </tbody>
        </Table>
    );
}

export default ChemTableComp