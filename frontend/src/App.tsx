import { BrowserRouter } from 'react-router'
import Routing from '@/components/routing'
import { Authprovider } from '@/contexts/AuthContext'
import { SettingsProvider } from '@/contexts/SettingsContext'
import './App.css'

const App = () => (
    <BrowserRouter>
        <Authprovider>
            <SettingsProvider>
                <Routing />
            </SettingsProvider>
        </Authprovider>
    </BrowserRouter>
)
export default App
