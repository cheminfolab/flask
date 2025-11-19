import { BrowserRouter } from 'react-router'
import Routing from '@/components/routing'
import { Authprovider } from '@/contexts/AuthContext'
import './App.css'

const App = () => (
    <BrowserRouter>
        <Authprovider>
            <Routing />
        </Authprovider>
    </BrowserRouter>
)
export default App
