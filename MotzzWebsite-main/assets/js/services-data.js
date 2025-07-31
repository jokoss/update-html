// Services Data Structure
const servicesData = {
    agriculture: {
        id: 'agriculture',
        title: 'Agriculture',
        subtitle: 'Farm, Golf Course & Nursery Testing',
        description: 'Comprehensive testing services for soil, plant, water, compost/mulch and fertilizer. We provide services to most of the farms, golf courses, and nurseries in Arizona and some parts of Nevada and California.',
        icon: 'farming.svg',
        color: '#22c55e',
        testCount: 12,
        turnaround: '3-7 days',
        popularity: 95,
        popularTests: ['Soil Analysis', 'Plant Tissue', 'Water Quality'],
        categories: {
            soil: {
                name: 'Soil Analysis',
                icon: 'soil.svg',
                description: 'Complete soil testing for nutrient content, pH, and soil health assessment.',
                tests: [
                    {
                        name: 'Basic Soil Package',
                        price: '$45',
                        turnaround: '3-5 days',
                        description: 'Essential soil nutrients and pH testing',
                        features: ['pH Level', 'Organic Matter', 'Phosphorus', 'Potassium', 'Recommendations']
                    },
                    {
                        name: 'Complete Soil Analysis',
                        price: '$85',
                        turnaround: '5-7 days',
                        description: 'Comprehensive soil analysis with micronutrients',
                        features: ['All Basic Package items', 'Micronutrients', 'Heavy Metals', 'Salinity', 'CEC', 'Detailed Report']
                    },
                    {
                        name: 'Heavy Metals Screening',
                        price: '$120',
                        turnaround: '7-10 days',
                        description: 'Specialized testing for heavy metal contamination',
                        features: ['Lead', 'Cadmium', 'Mercury', 'Arsenic', 'Chromium', 'Compliance Report']
                    }
                ]
            },
            plant: {
                name: 'Plant/Tissue Analysis',
                icon: 'plant.svg',
                description: 'Plant tissue and petiole analysis for nutrient deficiency diagnosis.',
                tests: [
                    {
                        name: 'Plant Tissue Analysis',
                        price: '$35',
                        turnaround: '3-5 days',
                        description: 'Complete plant nutrient analysis',
                        features: ['Nitrogen', 'Phosphorus', 'Potassium', 'Micronutrients', 'Recommendations']
                    },
                    {
                        name: 'Petiole Analysis',
                        price: '$30',
                        turnaround: '3-5 days',
                        description: 'Petiole testing for real-time nutrient status',
                        features: ['Nitrate-N', 'Phosphorus', 'Potassium', 'Quick Results', 'Growing Season Monitoring']
                    }
                ]
            },
            water: {
                name: 'Water Quality',
                icon: 'water-drop.svg',
                description: 'Irrigation water quality testing for agricultural use.',
                tests: [
                    {
                        name: 'Irrigation Water Analysis',
                        price: '$55',
                        turnaround: '3-5 days',
                        description: 'Complete irrigation water quality assessment',
                        features: ['pH', 'EC', 'Sodium', 'Chloride', 'Boron', 'SAR Calculation']
                    },
                    {
                        name: 'Well Water Testing',
                        price: '$75',
                        turnaround: '5-7 days',
                        description: 'Comprehensive well water analysis',
                        features: ['All Irrigation items', 'Heavy Metals', 'Bacteria', 'Nitrates', 'Safety Assessment']
                    }
                ]
            },
            compost: {
                name: 'Compost/Mulch',
                icon: 'composting.svg',
                description: 'Compost and mulch quality testing for soil amendment.',
                tests: [
                    {
                        name: 'Available Nutrients',
                        price: '$65',
                        turnaround: '5-7 days',
                        description: 'Available nutrient content in compost',
                        features: ['Available N-P-K', 'pH', 'EC', 'Organic Matter', 'Application Rates']
                    },
                    {
                        name: 'Total Nutrients',
                        price: '$85',
                        turnaround: '7-10 days',
                        description: 'Complete nutrient profile analysis',
                        features: ['Total N-P-K', 'Micronutrients', 'Heavy Metals', 'Maturity Index', 'Quality Assessment']
                    }
                ]
            },
            fertilizer: {
                name: 'Fertilizer Analysis',
                icon: 'fertilizer.svg',
                description: 'Liquid and solid fertilizer testing for quality assurance.',
                tests: [
                    {
                        name: 'Liquid Fertilizer',
                        price: '$45',
                        turnaround: '3-5 days',
                        description: 'Liquid fertilizer nutrient verification',
                        features: ['N-P-K Content', 'pH', 'Micronutrients', 'Label Verification', 'Quality Report']
                    },
                    {
                        name: 'Solid Fertilizer',
                        price: '$55',
                        turnaround: '5-7 days',
                        description: 'Granular fertilizer analysis',
                        features: ['Total N-P-K', 'Slow Release N', 'Micronutrients', 'Physical Properties', 'Compliance Testing']
                    }
                ]
            }
        }
    },
    environmental: {
        id: 'environmental',
        title: 'Environmental',
        subtitle: 'Water & Environmental Testing',
        description: 'Safe Drinking Water, Well Water, Waste Water, and Solid Waste testing services for environmental compliance and safety.',
        icon: 'environmental-water.svg',
        color: '#3b82f6',
        testCount: 8,
        turnaround: '5-10 days',
        popularity: 85,
        popularTests: ['Drinking Water', 'Well Water', 'Wastewater'],
        categories: {
            drinking: {
                name: 'Drinking Water',
                icon: 'water-drop.svg',
                description: 'Safe drinking water testing for compliance and safety.',
                tests: [
                    {
                        name: 'Basic Water Safety',
                        price: '$95',
                        turnaround: '5-7 days',
                        description: 'Essential drinking water safety tests',
                        features: ['Bacteria', 'pH', 'Chlorine', 'Turbidity', 'Basic Metals', 'Safety Report']
                    },
                    {
                        name: 'Complete Water Analysis',
                        price: '$185',
                        turnaround: '7-10 days',
                        description: 'Comprehensive drinking water testing',
                        features: ['All Basic items', 'Heavy Metals', 'Pesticides', 'VOCs', 'EPA Compliance', 'Detailed Report']
                    }
                ]
            },
            well: {
                name: 'Well Water',
                icon: 'water-drop.svg',
                description: 'Private well water testing for homeowners and businesses.',
                tests: [
                    {
                        name: 'Well Water Package',
                        price: '$125',
                        turnaround: '5-7 days',
                        description: 'Standard well water testing package',
                        features: ['Bacteria', 'Nitrates', 'pH', 'Hardness', 'Iron', 'Manganese', 'Recommendations']
                    }
                ]
            },
            wastewater: {
                name: 'Wastewater',
                icon: 'environmental-water.svg',
                description: 'Wastewater testing for treatment and compliance.',
                tests: [
                    {
                        name: 'Wastewater Analysis',
                        price: '$155',
                        turnaround: '7-10 days',
                        description: 'Complete wastewater characterization',
                        features: ['BOD', 'COD', 'TSS', 'pH', 'Nutrients', 'Heavy Metals', 'Compliance Report']
                    }
                ]
            }
        }
    },
    construction: {
        id: 'construction',
        title: 'Construction Materials',
        subtitle: 'Soil & Aggregate Testing',
        description: 'With our engineering background, we perform soil aggregate testing using ADOT, CDOT, AASHTO and ASTM specified methods.',
        icon: 'dump-truck.svg',
        color: '#f59e0b',
        testCount: 6,
        turnaround: '3-7 days',
        popularity: 70,
        popularTests: ['Soil Compaction', 'Aggregate Testing', 'Concrete Testing'],
        categories: {
            soil: {
                name: 'Soil Testing',
                icon: 'soil.svg',
                description: 'Geotechnical soil testing for construction projects.',
                tests: [
                    {
                        name: 'Proctor Compaction',
                        price: '$85',
                        turnaround: '3-5 days',
                        description: 'Standard Proctor compaction testing',
                        features: ['Maximum Density', 'Optimum Moisture', 'ASTM D698', 'Compaction Curve', 'Engineering Report']
                    },
                    {
                        name: 'California Bearing Ratio',
                        price: '$125',
                        turnaround: '5-7 days',
                        description: 'CBR testing for pavement design',
                        features: ['CBR Value', 'Soaked/Unsoaked', 'ASTM D1883', 'Swell Measurement', 'Design Parameters']
                    }
                ]
            },
            aggregate: {
                name: 'Aggregate Testing',
                icon: 'dump-truck.svg',
                description: 'Aggregate quality testing for construction materials.',
                tests: [
                    {
                        name: 'Gradation Analysis',
                        price: '$65',
                        turnaround: '3-5 days',
                        description: 'Sieve analysis for aggregate gradation',
                        features: ['Sieve Analysis', 'Fineness Modulus', 'ASTM C136', 'Gradation Curve', 'Specification Compliance']
                    }
                ]
            }
        }
    },
    dietary: {
        id: 'dietary',
        title: 'Dietary Supplements',
        subtitle: 'Nutraceutical & Vitamin Testing',
        description: 'Minerals, Contaminants, Heavy Metals, and Microbiology testing for dietary supplements and nutraceuticals.',
        icon: 'vitamin.svg',
        color: '#8b5cf6',
        testCount: 5,
        turnaround: '7-14 days',
        popularity: 60,
        popularTests: ['Heavy Metals', 'Micronutrients', 'Contaminants'],
        categories: {
            minerals: {
                name: 'Mineral Analysis',
                icon: 'vitamin.svg',
                description: 'Mineral and vitamin content verification.',
                tests: [
                    {
                        name: 'Vitamin Analysis',
                        price: '$145',
                        turnaround: '7-10 days',
                        description: 'Vitamin content verification',
                        features: ['Vitamin A', 'Vitamin C', 'Vitamin D', 'B-Complex', 'Label Verification', 'Potency Testing']
                    },
                    {
                        name: 'Mineral Content',
                        price: '$125',
                        turnaround: '7-10 days',
                        description: 'Essential mineral analysis',
                        features: ['Calcium', 'Iron', 'Zinc', 'Magnesium', 'Trace Elements', 'Bioavailability']
                    }
                ]
            },
            contaminants: {
                name: 'Contaminant Testing',
                icon: 'vitamin.svg',
                description: 'Heavy metals and contaminant screening.',
                tests: [
                    {
                        name: 'Heavy Metals Panel',
                        price: '$165',
                        turnaround: '10-14 days',
                        description: 'Comprehensive heavy metals testing',
                        features: ['Lead', 'Mercury', 'Cadmium', 'Arsenic', 'FDA Limits', 'Safety Assessment']
                    }
                ]
            }
        }
    },
    microbiology: {
        id: 'microbiology',
        title: 'Microbiology',
        subtitle: 'Microbiological Testing',
        description: 'Microbiological testing for fertilizer, drinking water, and other samples requiring bacterial analysis.',
        icon: 'bacteria.svg',
        color: '#ef4444',
        testCount: 4,
        turnaround: '3-7 days',
        popularity: 75,
        popularTests: ['Bacteria Testing', 'Pathogen Screening', 'Water Microbiology'],
        categories: {
            water: {
                name: 'Water Microbiology',
                icon: 'bacteria.svg',
                description: 'Bacterial testing for water samples.',
                tests: [
                    {
                        name: 'Coliform Testing',
                        price: '$45',
                        turnaround: '3-5 days',
                        description: 'Total and fecal coliform testing',
                        features: ['Total Coliforms', 'E. coli', 'Fecal Coliforms', 'EPA Method', 'Safety Assessment']
                    }
                ]
            },
            fertilizer: {
                name: 'Fertilizer Microbiology',
                icon: 'bacteria.svg',
                description: 'Microbiological testing for organic fertilizers.',
                tests: [
                    {
                        name: 'Pathogen Screening',
                        price: '$85',
                        turnaround: '5-7 days',
                        description: 'Pathogen testing for organic fertilizers',
                        features: ['Salmonella', 'E. coli', 'Fecal Coliforms', 'Organic Certification', 'Safety Report']
                    }
                ]
            }
        }
    },
    research: {
        id: 'research',
        title: 'Research & Development',
        subtitle: 'Custom Testing Solutions',
        description: 'Method Development and Stability Study services for specialized research and development projects.',
        icon: 'research.svg',
        color: '#06b6d4',
        testCount: 3,
        turnaround: '14-30 days',
        popularity: 40,
        popularTests: ['Method Development', 'Stability Studies', 'Custom Analysis'],
        categories: {
            method: {
                name: 'Method Development',
                icon: 'research.svg',
                description: 'Custom analytical method development.',
                tests: [
                    {
                        name: 'Custom Method Development',
                        price: 'Quote',
                        turnaround: '14-30 days',
                        description: 'Development of custom analytical methods',
                        features: ['Method Design', 'Validation', 'Documentation', 'Training', 'Technical Support']
                    }
                ]
            },
            stability: {
                name: 'Stability Studies',
                icon: 'research.svg',
                description: 'Product stability and shelf-life testing.',
                tests: [
                    {
                        name: 'Stability Testing',
                        price: 'Quote',
                        turnaround: '30+ days',
                        description: 'Long-term stability studies',
                        features: ['Accelerated Testing', 'Real-time Studies', 'Statistical Analysis', 'Shelf-life Determination', 'Regulatory Support']
                    }
                ]
            }
        }
    }
};

// Search keywords for better search functionality
const searchKeywords = {
    agriculture: ['soil', 'plant', 'tissue', 'petiole', 'water', 'irrigation', 'compost', 'mulch', 'fertilizer', 'farm', 'golf', 'nursery', 'crop', 'nutrient', 'pH', 'organic matter'],
    environmental: ['drinking water', 'well water', 'wastewater', 'bacteria', 'heavy metals', 'pesticides', 'VOCs', 'EPA', 'compliance', 'safety', 'contamination'],
    construction: ['soil compaction', 'aggregate', 'concrete', 'proctor', 'CBR', 'gradation', 'ASTM', 'AASHTO', 'ADOT', 'CDOT', 'geotechnical', 'pavement'],
    dietary: ['vitamin', 'mineral', 'supplement', 'nutraceutical', 'heavy metals', 'contaminants', 'potency', 'label verification', 'FDA', 'bioavailability'],
    microbiology: ['bacteria', 'coliform', 'E. coli', 'pathogen', 'salmonella', 'microbiological', 'organic certification', 'water bacteria'],
    research: ['method development', 'stability', 'custom analysis', 'validation', 'R&D', 'research', 'development', 'shelf life', 'accelerated testing']
};

// Popular services for quick access
const popularServices = [
    { category: 'agriculture', subcategory: 'soil', test: 'Complete Soil Analysis' },
    { category: 'agriculture', subcategory: 'plant', test: 'Plant Tissue Analysis' },
    { category: 'environmental', subcategory: 'drinking', test: 'Basic Water Safety' },
    { category: 'construction', subcategory: 'soil', test: 'Proctor Compaction' },
    { category: 'dietary', subcategory: 'contaminants', test: 'Heavy Metals Panel' },
    { category: 'microbiology', subcategory: 'water', test: 'Coliform Testing' }
];

// Service categories for filtering
const serviceCategories = [
    { id: 'all', name: 'All Services', count: 0 },
    { id: 'agriculture', name: 'Agriculture', count: 12 },
    { id: 'environmental', name: 'Environmental', count: 8 },
    { id: 'construction', name: 'Construction', count: 6 },
    { id: 'dietary', name: 'Dietary', count: 5 },
    { id: 'microbiology', name: 'Microbiology', count: 4 },
    { id: 'research', name: 'Research', count: 3 }
];

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { servicesData, searchKeywords, popularServices, serviceCategories };
}
