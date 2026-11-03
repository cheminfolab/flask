/**
 * Backend data types, generated from the OpenAPI schema.
 *
 * Do not write these by hand: regenerate with `npm run gen:api` after the
 * backend changes (CI fails if `api.gen.ts` is out of date).
 */
import type { components } from "./api.gen"

type Schemas = components["schemas"]

export type Id = number

// accounts
export type Member = Schemas["Member"]
export type MemberDirectoryEntry = Schemas["MemberDirectory"]
export type WorkingGroup = Schemas["WorkingGroup"]
export type RegistrationPayload = Schemas["RegistrationRequest"]

// chemicals & locations
export type Unit = Schemas["Unit"]
export type Substance = Schemas["Substance"]
export type Component = Schemas["Component"]
export type Compound = Schemas["Compound"]
export type Container = Schemas["Container"]
export type Storage = Schemas["Storage"]

// notebook
export type Project = Schemas["Project"]
export type ProjectRequest = Schemas["ProjectRequest"]
export type ProjectShare = Schemas["ProjectShare"]
export type Experiment = Schemas["Experiment"]
export type ExperimentShare = Schemas["ExperimentShare"]
export type Entry = Schemas["Entry"]
export type MaterialUsage = Schemas["MaterialUsage"]
export type Attachment = Schemas["Attachment"]
