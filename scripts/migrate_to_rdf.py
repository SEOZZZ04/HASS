"""
Maritime Data to RDF Migration Script
Converts existing JSON data (colregs, cases, scenarios) to RDF/Turtle format
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL


class MaritimeDataToRDF:
    """Convert maritime JSON data to RDF ontology format"""

    def __init__(self):
        # Initialize graph
        self.graph = Graph()

        # Define namespaces
        self.MSO = Namespace("http://weoffice.ai/ontology/maritime-safety#")
        self.COLREG = Namespace("http://weoffice.ai/ontology/colregs#")

        # Bind namespaces
        self.graph.bind("mso", self.MSO)
        self.graph.bind("colreg", self.COLREG)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("xsd", XSD)
        self.graph.bind("owl", OWL)

        # Data paths
        self.data_dir = Path("/home/user/HASS/data/raw")
        self.output_dir = Path("/home/user/HASS/data/ontology")
        self.output_dir.mkdir(exist_ok=True, parents=True)

    def load_json(self, filename: str) -> Any:
        """Load JSON file"""
        with open(self.data_dir / filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def convert_regulations(self):
        """Convert COLREGs rules to RDF Regulation entities"""
        print("Converting COLREGs regulations to RDF...")

        rules = self.load_json("colregs_rules.json")

        for rule in rules:
            rule_id = rule['id']  # e.g., "rule_05"
            rule_uri = self.COLREG[rule_id.replace("_", "-")]  # colreg:rule-05

            # Create Regulation entity
            self.graph.add((rule_uri, RDF.type, self.MSO.Regulation))
            self.graph.add((rule_uri, self.MSO.regulationId, Literal(rule_id)))
            self.graph.add((rule_uri, self.MSO.titleKr, Literal(rule['title'], lang='ko')))
            self.graph.add((rule_uri, self.MSO.titleEn, Literal(rule.get('title_en', ''), lang='en')))
            self.graph.add((rule_uri, self.MSO.category, Literal(rule['category'])))
            self.graph.add((rule_uri, self.MSO.fullTextKr, Literal(rule['full_text'], lang='ko')))
            self.graph.add((rule_uri, self.MSO.legalWeight, Literal(rule['legal_weight'], datatype=XSD.integer)))

            # Create SafetyIssue relationships
            if 'addresses_issues' in rule:
                for issue_name in rule['addresses_issues']:
                    issue_uri = self.MSO[self._create_uri_id(issue_name)]
                    self.graph.add((issue_uri, RDF.type, self.MSO.SafetyIssue))
                    self.graph.add((issue_uri, self.MSO.nameKr, Literal(issue_name, lang='ko')))
                    self.graph.add((rule_uri, self.MSO.addresses, issue_uri))

            # Create Action recommendations
            if 'recommended_actions' in rule:
                for action_name in rule['recommended_actions']:
                    action_uri = self.MSO[self._create_uri_id(f"action-{action_name}")]
                    self.graph.add((action_uri, RDF.type, self.MSO.Action))
                    self.graph.add((action_uri, self.MSO.nameKr, Literal(action_name, lang='ko')))
                    self.graph.add((action_uri, self.MSO.recommendedBy, rule_uri))

        print(f"✓ Converted {len(rules)} regulations")

    def convert_cases(self):
        """Convert maritime accident cases to RDF MaritimeCase entities"""
        print("Converting maritime cases to RDF...")

        cases = self.load_json("kmst_cases.json")

        for case in cases:
            case_id = case['case_id']
            case_uri = self.MSO[case_id.replace("-", "_")]

            # Create MaritimeCase entity
            self.graph.add((case_uri, RDF.type, self.MSO.MaritimeCase))
            self.graph.add((case_uri, self.MSO.caseId, Literal(case_id)))
            self.graph.add((case_uri, self.MSO.titleKr, Literal(case['title'], lang='ko')))
            self.graph.add((case_uri, self.MSO.date, Literal(case['date'], datatype=XSD.date)))
            self.graph.add((case_uri, self.MSO.location, Literal(case['location'], lang='ko')))
            self.graph.add((case_uri, self.MSO.description, Literal(case['incident_description'], lang='ko')))
            self.graph.add((case_uri, self.MSO.judgment, Literal(case['judgment'], lang='ko')))
            self.graph.add((case_uri, self.MSO.penalty, Literal(case['penalty'], lang='ko')))
            self.graph.add((case_uri, self.MSO.legalWeight, Literal(case['legal_weight'], datatype=XSD.integer)))

            # Link to violated regulations
            if 'violated_rules' in case:
                for rule_id in case['violated_rules']:
                    rule_uri = self.COLREG[rule_id.replace("_", "-")]
                    self.graph.add((case_uri, self.MSO.violated, rule_uri))

            # Create Lessons
            if 'lessons' in case:
                for idx, lesson_text in enumerate(case['lessons']):
                    lesson_uri = self.MSO[f"lesson-{case_id}-{idx}"]
                    self.graph.add((lesson_uri, RDF.type, self.MSO.Lesson))
                    self.graph.add((lesson_uri, self.MSO.textKr, Literal(lesson_text, lang='ko')))
                    self.graph.add((lesson_uri, self.MSO.importance, Literal(8, datatype=XSD.integer)))
                    self.graph.add((case_uri, self.MSO.teaches, lesson_uri))

            # Create SafetyIssue relationship
            if 'situation_type' in case:
                situation = case['situation_type']
                if isinstance(situation, list):
                    for sit in situation:
                        issue_uri = self.MSO[self._create_uri_id(sit)]
                        self.graph.add((issue_uri, RDF.type, self.MSO.SafetyIssue))
                        self.graph.add((issue_uri, self.MSO.nameKr, Literal(sit, lang='ko')))
                        self.graph.add((case_uri, self.MSO.exampleOf, issue_uri))
                else:
                    issue_uri = self.MSO[self._create_uri_id(situation)]
                    self.graph.add((issue_uri, RDF.type, self.MSO.SafetyIssue))
                    self.graph.add((issue_uri, self.MSO.nameKr, Literal(situation, lang='ko')))
                    self.graph.add((case_uri, self.MSO.exampleOf, issue_uri))

            # Create Vessel entities
            if 'vessels_involved' in case:
                for vessel_info in case['vessels_involved']:
                    vessel_uri = self.MSO[self._create_uri_id(f"vessel-{vessel_info['type']}")]
                    self.graph.add((vessel_uri, RDF.type, self.MSO.Vessel))
                    self.graph.add((vessel_uri, self.MSO.vesselType, Literal(vessel_info['type'])))
                    self.graph.add((case_uri, self.MSO.involves, vessel_uri))

        print(f"✓ Converted {len(cases)} maritime cases")

    def create_additional_relationships(self):
        """Create inferred relationships between entities"""
        print("Creating additional semantic relationships...")

        # Link regulations that cite each other
        # Rule 15 (Crossing) relates to Rule 16 (Give-way) and Rule 17 (Stand-on)
        self.graph.add((
            self.COLREG["rule-15"],
            self.MSO.relatedTo,
            self.COLREG["rule-16"]
        ))
        self.graph.add((
            self.COLREG["rule-15"],
            self.MSO.relatedTo,
            self.COLREG["rule-17"]
        ))

        # Rule 19 (Restricted Visibility) relates to Rule 5 (Look-out) and Rule 6 (Safe Speed)
        self.graph.add((
            self.COLREG["rule-19"],
            self.MSO.relatedTo,
            self.COLREG["rule-05"]
        ))
        self.graph.add((
            self.COLREG["rule-19"],
            self.MSO.relatedTo,
            self.COLREG["rule-06"]
        ))

        print("✓ Added semantic relationships")

    def _create_uri_id(self, text: str) -> str:
        """Create URI-safe identifier from Korean/English text"""
        # Simple approach: remove spaces and special characters
        import re
        uri_id = re.sub(r'[^\w가-힣]', '_', text)
        uri_id = uri_id.lower().replace(' ', '_')
        return uri_id

    def save_to_file(self, filename: str = "maritime_data.ttl"):
        """Save RDF graph to Turtle file"""
        output_path = self.output_dir / filename
        self.graph.serialize(destination=str(output_path), format='turtle')
        print(f"\n✓ RDF data saved to: {output_path}")
        print(f"  Total triples: {len(self.graph)}")

    def run_migration(self):
        """Run full migration process"""
        print("=" * 60)
        print("Maritime Data to RDF Migration")
        print("=" * 60)
        print()

        # Convert data
        self.convert_regulations()
        self.convert_cases()
        self.create_additional_relationships()

        # Save to file
        self.save_to_file("maritime_data.ttl")

        # Print statistics
        print("\n" + "=" * 60)
        print("Migration Statistics")
        print("=" * 60)

        # Count entity types
        entity_counts = {}
        for entity_type in [
            self.MSO.Regulation, self.MSO.MaritimeCase, self.MSO.SafetyIssue,
            self.MSO.Lesson, self.MSO.Action, self.MSO.Vessel
        ]:
            count = len(list(self.graph.subjects(RDF.type, entity_type)))
            entity_name = str(entity_type).split('#')[-1]
            entity_counts[entity_name] = count
            print(f"  {entity_name}: {count}")

        print("\n✓ Migration completed successfully!")
        print("=" * 60)


def main():
    """Main execution"""
    migrator = MaritimeDataToRDF()
    migrator.run_migration()


if __name__ == "__main__":
    main()
