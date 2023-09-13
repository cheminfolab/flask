export type Id = number

export interface Unit {
    id: Id
    name: string
    symbol: string
}

export interface Substance {
    id: Id
    name: string
    synonyms: string[]
    label: string
    formula: string
    cas: string
    pubchem_sid: null
    mol_weight: number
    exact_mass: number
    image: string
    mol_weight_unit: number
    exact_mass_unit: number
    structure: number[]
}

export interface Component {
    fraction: number
    type: string
    substance: number
}

export interface Compound {
    id: Id
    substances: Component[]
    name: string
    synonyms: string[]
    label: string
    purity: number
    pubchem_cid: number
    density: number
    color: string
    melting_point: number
    boiling_point: number
    flash_point: number
    created: string
    density_unit: number
    melting_point_unit: number
    boiling_point_unit: number
    flash_point_unit: number
    ghs: number
    created_by: number
    categories: number[]
}