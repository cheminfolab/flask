import {Col, Container, Form, Modal, Row, Tab, Tabs} from "react-bootstrap";
import './ChemDetailComp.css';
import SubstanceImage from "./SubstanceImage";

export default function ChemDetailComp({show, setShow, compoundDetail}) {

  let {id, density_unit, currency, owner, pubchem_cid, density, purity, opened, price, annotation,
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
    } = compoundDetail

  return (
    <>
      {/* todo: use fullscreen below X (https://react-bootstrap.github.io/components/modal/) */}

      <Modal
        show={show}
        onHide={() => setShow(false)}
        dialogClassName="modal-90w"
        aria-labelledby="example-custom-modal-styling-title"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-custom-modal-styling-title">
            Detailed Compound View
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Container>
            <Row>
              <Col xs={12} lg={2}>
                {(image ? <SubstanceImage path={image}/>: 'IMAGE')}
              </Col>
              <Col xs={12} lg={10}>
                <p>
                  Ipsum molestiae natus adipisci modi eligendi? Debitis amet quae unde
                  commodi aspernatur enim, consectetur. Cumque deleniti temporibus
                  ipsam atque a dolores quisquam quisquam adipisci possimus
                  laboriosam. Quibusdam facilis doloribus debitis! Sit quasi quod
                  accusamus eos quod. Ab quos consequuntur eaque quo rem! Mollitia
                  reiciendis porro quo magni incidunt dolore amet atque facilis ipsum
                  deleniti rem!
                </p>
              </Col>
            </Row>
          </Container>
          <Tabs
            defaultActiveKey="home"
            transition={false}
            id="noanim-tab-example"
            className="mb-3"
          >
            <Tab eventKey="home" title="Properties">
                <p>
                  Ipsum molestiae natus adipisci modi eligendi? Debitis amet quae unde
                  commodi aspernatur enim, consectetur. Cumque deleniti temporibus
                  ipsam atque a dolores quisquam quisquam adipisci possimus
                  laboriosam. Quibusdam facilis doloribus debitis! Sit quasi quod
                  accusamus eos quod. Ab quos consequuntur eaque quo rem! Mollitia
                  reiciendis porro quo magni incidunt dolore amet atque facilis ipsum
                  deleniti rem!
                </p>
            </Tab>
            <Tab eventKey="profile" title="Spectra">
                <p>
                  Ipsum molestiae natus adipisci modi eligendi? Debitis amet quae unde
                  commodi aspernatur enim, consectetur. Cumque deleniti temporibus
                  ipsam atque a dolores quisquam quisquam adipisci possimus
                  laboriosam. Quibusdam facilis doloribus debitis! Sit quasi quod
                  accusamus eos quod. Ab quos consequuntur eaque quo rem! Mollitia
                  reiciendis porro quo magni incidunt dolore amet atque facilis ipsum
                  deleniti rem!
                </p>
            </Tab>
            <Tab eventKey="contact" title="SDS">
                <p>
                  Ipsum molestiae natus adipisci modi eligendi? Debitis amet quae unde
                  commodi aspernatur enim, consectetur. Cumque deleniti temporibus
                  ipsam atque a dolores quisquam quisquam adipisci possimus
                  laboriosam. Quibusdam facilis doloribus debitis! Sit quasi quod
                  accusamus eos quod. Ab quos consequuntur eaque quo rem! Mollitia
                  reiciendis porro quo magni incidunt dolore amet atque facilis ipsum
                  deleniti rem!
                </p>
            </Tab>
          </Tabs>
          <Container>
            <Row>
              <Col xs={12} md={8}>
                .col-xs-12 .col-md-8
              </Col>
              <Col xs={6} md={4}>
                .col-xs-6 .col-md-4
              </Col>
            </Row>

            <Row>
              <Col xs={6} md={4}>
                .col-xs-6 .col-md-4
              </Col>
              <Col xs={6} md={4}>
                .col-xs-6 .col-md-4
              </Col>
              <Col xs={6} md={4}>
                .col-xs-6 .col-md-4
              </Col>
            </Row>
          </Container>
          <Form>
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                name="email2"
                placeholder="name@example.com"
                autoFocus
              />
            </Form.Group>
            <Form.Group
                name="text_area"
                className="mb-3"
                controlId="exampleForm.ControlTextarea1"
            >
              <Form.Label>Example textarea</Form.Label>
              <Form.Control as="textarea" rows={3} />
            </Form.Group>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
}