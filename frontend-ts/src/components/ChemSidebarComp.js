import {Accordion, Button, Form, FormControl} from "react-bootstrap";
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
                  {['checkbox', 'radio'].map((type) => (
                    <div key={`default-${type}`} className="mb-3">
                      <Form.Check
                        type={type}
                        id={`default-${type}`}
                        label={`default ${type}`}
                      />

                      <Form.Check
                        disabled
                        type={type}
                        label={`disabled ${type}`}
                        id={`disabled-default-${type}`}
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
        // <div className="flex-shrink-0 p-3 bg-white">
        //     <a href="/" className="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom">
        //         <svg className="bi me-2" width="30" height="24"></svg>
        //         <span className="fs-5 fw-semibold">Collapsible</span>
        //     </a>
        //     <ul className="list-unstyled ps-0">
        //         <li className="mb-1">
        //             <Button className="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse"
        //                     data-bs-target="#home-collapse" aria-expanded="false">
        //                 Home
        //             </Button>
        //             <div className="collapse" id="home-collapse">
        //                 <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
        //                     <li><a href="#" className="link-dark rounded">Overview</a></li>
        //                     <li><a href="#" className="link-dark rounded">Updates</a></li>
        //                     <li><a href="#" className="link-dark rounded">Reports</a></li>
        //                 </ul>
        //             </div>
        //         </li>
        //         <li className="mb-1">
        //             <Button className="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse"
        //                     data-bs-target="#dashboard-collapse" aria-expanded="false">
        //                 Dashboard
        //             </Button>
        //             <div className="collapse" id="dashboard-collapse">
        //                 <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
        //                     <li><a href="#" className="link-dark rounded">Overview</a></li>
        //                     <li><a href="#" className="link-dark rounded">Weekly</a></li>
        //                     <li><a href="#" className="link-dark rounded">Monthly</a></li>
        //                     <li><a href="#" className="link-dark rounded">Annually</a></li>
        //                 </ul>
        //             </div>
        //         </li>
        //         <li className="mb-1">
        //             <Button className="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse"
        //                     data-bs-target="#orders-collapse" aria-expanded="false">
        //                 Orders
        //             </Button>
        //             <div className="collapse" id="orders-collapse">
        //                 <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
        //                     <li><a href="#" className="link-dark rounded">New</a></li>
        //                     <li><a href="#" className="link-dark rounded">Processed</a></li>
        //                     <li><a href="#" className="link-dark rounded">Shipped</a></li>
        //                     <li><a href="#" className="link-dark rounded">Returned</a></li>
        //                 </ul>
        //             </div>
        //         </li>
        //         <li className="border-top my-3"></li>
        //         <li className="mb-1">
        //             <Button className="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse"
        //                     data-bs-target="#account-collapse" aria-expanded="false">
        //                 Account
        //             </Button>
        //             <div className="collapse" id="account-collapse">
        //                 <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
        //                     <li><a href="#" className="link-dark rounded">New...</a></li>
        //                     <li><a href="#" className="link-dark rounded">Profile</a></li>
        //                     <li><a href="#" className="link-dark rounded">Settings</a></li>
        //                     <li><a href="#" className="link-dark rounded">Sign out</a></li>
        //                 </ul>
        //             </div>
        //         </li>
        //     </ul>
        //
        //
        //     {/*<h2>Wiki</h2>*/}
        //     {/*<form action="">*/}
        //     {/*    <input className="search" type="text" name="q" placeholder="Search Encyclopedia"/>*/}
        //     {/*</form>*/}
        //
        //
        //
        //     <ul className="list-unstyled ps-0 border-bottom">
        //         <li className="mb-1">
        //             <a className="btn btn-toggle align-items-center rounded collapsed"
        //                href="">Home</a>
        //         </li>
        //         <li className="mb-1">
        //             <a className="btn btn-toggle align-items-center rounded collapsed" href="">Create
        //                 New Page</a>
        //         </li>
        //         <li className="mb-1">
        //             <a className="btn btn-toggle align-items-center rounded collapsed"
        //                href="">Random Page</a>
        //         </li>
        //     </ul>
        //
        //
        // </div>
    )
}

export default ChemSidebarComp