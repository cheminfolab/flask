import {Accordion, Form, FormControl} from "react-bootstrap";
// https://getbootstrap.com/docs/5.0/examples/sidebars/#
// https://stackoverflow.com/questions/60482018/make-a-sidebar-from-react-bootstrap

const ChemSidebarComp = () => {
    return(
        <div>
        <h3>Chemicals</h3>
        <Accordion defaultActiveKey={['0']} alwaysOpen>
          <Accordion.Item eventKey="0">
            <Accordion.Header>Filter</Accordion.Header>
            <Accordion.Body>
                <Form>
                    <FormControl
                      type="search"
                      placeholder="CAS, InChI, name..."
                      className="me-2 mb-3"
                      aria-label="Search"
                    />
                  { // todo: use FormCheckType
                    ["checkbox", "radio"].map((checkType: "checkbox" | "radio" | "switch") => (
                    <div key={`default-${checkType}`} className="mb-3">
                      <Form.Check
                        type={checkType}
                        id={`default-${checkType}`}
                        label={`default ${checkType}`}
                      />

                      <Form.Check
                        disabled
                        type={checkType}
                        label={`disabled ${checkType}`}
                        id={`disabled-default-${checkType}`}
                      />
                    </div>
                  ))}
                  <Form.Check
                    type="switch"
                    id="custom-switch"
                    label="Check this switch"
                  />
                  <Form.Check
                    disabled
                    type="switch"
                    label="disabled switch"
                    id="disabled-custom-switch"
                  />
                </Form>
            </Accordion.Body>
          </Accordion.Item>
          <Accordion.Item eventKey="1">
            <Accordion.Header>Locations and Owners</Accordion.Header>
            <Accordion.Body>
                <Form.Check
                        type="radio"
                        id={`default-radio`}
                        label={"Huy"}
                      />
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
              minim veniam, quis nostrud exercitation ullamco laboris nisi ut
              aliquip ex ea commodo consequat. Duis aute irure dolor in
              reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
              pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
              culpa qui officia deserunt mollit anim id est laborum.
            </Accordion.Body>
          </Accordion.Item>
          <Accordion.Item eventKey="2">
            <Accordion.Header>Accordion Item #3</Accordion.Header>
            <Accordion.Body>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
              minim veniam, quis nostrud exercitation ullamco laboris nisi ut
              aliquip ex ea commodo consequat. Duis aute irure dolor in
              reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
              pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
              culpa qui officia deserunt mollit anim id est laborum.
            </Accordion.Body>
          </Accordion.Item>
        </Accordion>
        </div>
    )
}

export default ChemSidebarComp