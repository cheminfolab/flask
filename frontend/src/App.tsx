import { BrowserRouter } from 'react-router'
import Routing from '@/components/routing'
import './App.css'
import { Authprovider } from './contexts/AuthContext'

const App = () => (
    <BrowserRouter>
        <Authprovider>
            <Routing />
        </Authprovider>
    </BrowserRouter>
)
export default App
