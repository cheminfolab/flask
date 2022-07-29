import {Button} from "react-bootstrap";
// https://getbootstrap.com/docs/5.0/examples/sidebars/#
// https://stackoverflow.com/questions/60482018/make-a-sidebar-from-react-bootstrap

const ChemSidebarComp = () => {
    return(
        <div className="flex-shrink-0 p-3 bg-white" style={{width: 280}}>
            <a href="/" className="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom">
                <svg className="bi me-2" width="30" height="24"></svg>
                <span className="fs-5 fw-semibold">Collapsible</span>
            </a>
            <ul className="list-unstyled ps-0">
                <li className="mb-1">
                    <Button className="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse"
                            data-bs-target="#home-collapse" aria-expanded="false">
                        Home
                    </Button>
                    <div className="collapse" id="home-collapse">
                        <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                            <li><a href="#" className="link-dark rounded">Overview</a></li>
                            <li><a href="#" className="link-dark rounded">Updates</a></li>
                            <li><a href="#" className="link-dark rounded">Reports</a></li>
                        </ul>
                    </div>
                </li>
                <li className="mb-1">
                    <Button className="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse"
                            data-bs-target="#dashboard-collapse" aria-expanded="false">
                        Dashboard
                    </Button>
                    <div className="collapse" id="dashboard-collapse">
                        <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                            <li><a href="#" className="link-dark rounded">Overview</a></li>
                            <li><a href="#" className="link-dark rounded">Weekly</a></li>
                            <li><a href="#" className="link-dark rounded">Monthly</a></li>
                            <li><a href="#" className="link-dark rounded">Annually</a></li>
                        </ul>
                    </div>
                </li>
                <li className="mb-1">
                    <Button className="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse"
                            data-bs-target="#orders-collapse" aria-expanded="false">
                        Orders
                    </Button>
                    <div className="collapse" id="orders-collapse">
                        <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                            <li><a href="#" className="link-dark rounded">New</a></li>
                            <li><a href="#" className="link-dark rounded">Processed</a></li>
                            <li><a href="#" className="link-dark rounded">Shipped</a></li>
                            <li><a href="#" className="link-dark rounded">Returned</a></li>
                        </ul>
                    </div>
                </li>
                <li className="border-top my-3"></li>
                <li className="mb-1">
                    <Button className="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse"
                            data-bs-target="#account-collapse" aria-expanded="false">
                        Account
                    </Button>
                    <div className="collapse" id="account-collapse">
                        <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                            <li><a href="#" className="link-dark rounded">New...</a></li>
                            <li><a href="#" className="link-dark rounded">Profile</a></li>
                            <li><a href="#" className="link-dark rounded">Settings</a></li>
                            <li><a href="#" className="link-dark rounded">Sign out</a></li>
                        </ul>
                    </div>
                </li>
            </ul>


            {/*<h2>Wiki</h2>*/}
            {/*<form action="">*/}
            {/*    <input className="search" type="text" name="q" placeholder="Search Encyclopedia"/>*/}
            {/*</form>*/}



            <ul className="list-unstyled ps-0 border-bottom">
                <li className="mb-1">
                    <a className="btn btn-toggle align-items-center rounded collapsed"
                       href="">Home</a>
                </li>
                <li className="mb-1">
                    <a className="btn btn-toggle align-items-center rounded collapsed" href="">Create
                        New Page</a>
                </li>
                <li className="mb-1">
                    <a className="btn btn-toggle align-items-center rounded collapsed"
                       href="">Random Page</a>
                </li>
            </ul>


        </div>
    )
}

export default ChemSidebarComp