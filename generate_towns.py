#!/usr/bin/env python3
"""
Generate Bergen County town pages from homepage template with unique content
"""

import os
import re

# Town data: (name, slug, region, description, notable)
TOWNS = [
    ("Allendale", "allendale", "Northern Bergen County", "upscale residential borough", "tree-lined streets and family homes"),
    ("Alpine", "alpine", "Eastern Bergen County", "exclusive community along the Palisades", "luxury estates and scenic views"),
    ("Bergenfield", "bergenfield", "Central Bergen County", "diverse suburban community", "local shopping and residential neighborhoods"),
    ("Bogota", "bogota", "Southern Bergen County", "compact riverside borough", "close-knit community atmosphere"),
    ("Carlstadt", "carlstadt", "Southern Bergen County", "industrial and residential borough", "proximity to major highways"),
    ("Cliffside Park", "cliffside-park", "Eastern Bergen County", "densely populated borough", "Hudson River views and urban convenience"),
    ("Closter", "closter", "Northern Bergen County", "affluent residential community", "excellent schools and parks"),
    ("Cresskill", "cresskill", "Eastern Bergen County", "upscale suburban borough", "top-rated schools and quiet streets"),
    ("Demarest", "demarest", "Eastern Bergen County", "small residential community", "rural character and conservation areas"),
    ("Dumont", "dumont", "Central Bergen County", "family-oriented borough", "community events and local businesses"),
    ("East Rutherford", "east-rutherford", "Southern Bergen County", "home to MetLife Stadium", "sports venues and commercial districts"),
    ("Edgewater", "edgewater", "Eastern Bergen County", "waterfront community", "Hudson River access and modern developments"),
    ("Elmwood Park", "elmwood-park", "Southern Bergen County", "residential borough", "diverse neighborhoods and local shops"),
    ("Emerson", "emerson", "Central Bergen County", "quiet residential community", "suburban character and convenience"),
    ("Englewood", "englewood", "Eastern Bergen County", "diverse urban center", "cultural institutions and historic areas"),
    ("Englewood Cliffs", "englewood-cliffs", "Eastern Bergen County", "corporate headquarters location", "Palisades views and executive homes"),
    ("Fair Lawn", "fair-lawn", "Central Bergen County", "large residential borough", "excellent recreation facilities"),
    ("Fairview", "fairview", "Southern Bergen County", "diverse community", "convenient NYC access"),
    ("Fort Lee", "fort-lee", "Eastern Bergen County", "George Washington Bridge gateway", "high-rise living and dining options"),
    ("Franklin Lakes", "franklin-lakes", "Northwestern Bergen County", "affluent lakeside community", "luxury homes and natural beauty"),
    ("Garfield", "garfield", "Southern Bergen County", "working-class city", "diverse population and local industry"),
    ("Glen Rock", "glen-rock", "Central Bergen County", "desirable residential borough", "top schools and charming downtown"),
    ("Hackensack", "hackensack", "Bergen County Seat", "county seat and medical hub", "Hackensack University Medical Center"),
    ("Harrington Park", "harrington-park", "Northern Bergen County", "small residential borough", "quiet streets and community feel"),
    ("Hasbrouck Heights", "hasbrouck-heights", "Southern Bergen County", "charming downtown borough", "local shops and restaurants"),
    ("Haworth", "haworth", "Northern Bergen County", "exclusive residential community", "large properties and privacy"),
    ("Hillsdale", "hillsdale", "Northern Bergen County", "family-friendly borough", "parks and recreational programs"),
    ("Ho-Ho-Kus", "ho-ho-kus", "Central Bergen County", "historic upscale borough", "colonial architecture and boutiques"),
    ("Leonia", "leonia", "Eastern Bergen County", "artistic community", "creative residents and cultural events"),
    ("Little Ferry", "little-ferry", "Southern Bergen County", "waterfront borough", "Hackensack River access"),
    ("Lodi", "lodi", "Southern Bergen County", "diverse residential borough", "local businesses and community spirit"),
    ("Lyndhurst", "lyndhurst", "Southern Bergen County", "township with rich history", "diverse dining and shopping"),
    ("Mahwah", "mahwah", "Northwestern Bergen County", "largest Bergen County municipality", "corporate campuses and Ramapo Mountains"),
    ("Maywood", "maywood", "Southern Bergen County", "small residential borough", "tree-lined streets and local charm"),
    ("Midland Park", "midland-park", "Central Bergen County", "quiet residential community", "family neighborhoods and parks"),
    ("Montvale", "montvale", "Northern Bergen County", "corporate headquarters town", "business centers and residential areas"),
    ("Moonachie", "moonachie", "Southern Bergen County", "small industrial borough", "near Teterboro Airport"),
    ("New Milford", "new-milford", "Central Bergen County", "residential borough", "convenient location and local amenities"),
    ("North Arlington", "north-arlington", "Southern Bergen County", "residential borough", "easy NYC commute"),
    ("Northvale", "northvale", "Northern Bergen County", "small border community", "quiet residential streets"),
    ("Norwood", "norwood", "Northern Bergen County", "residential borough", "parks and community events"),
    ("Oakland", "oakland", "Northwestern Bergen County", "Ramapo Valley community", "outdoor recreation and natural settings"),
    ("Old Tappan", "old-tappan", "Northern Bergen County", "upscale residential borough", "large homes and excellent schools"),
    ("Oradell", "oradell", "Central Bergen County", "charming residential borough", "historic district and river access"),
    ("Palisades Park", "palisades-park", "Eastern Bergen County", "diverse borough", "Korean-American businesses and culture"),
    ("Paramus", "paramus", "Central Bergen County", "major retail destination", "shopping centers and corporate offices"),
    ("Park Ridge", "park-ridge", "Northern Bergen County", "residential borough", "community-focused neighborhoods"),
    ("Ramsey", "ramsey", "Northern Bergen County", "suburban borough", "historic Main Street and local shops"),
    ("Ridgefield", "ridgefield", "Southern Bergen County", "residential borough", "diverse community near NYC"),
    ("Ridgefield Park", "ridgefield-park", "Southern Bergen County", "village atmosphere", "tree-lined streets and local businesses"),
    ("Ridgewood", "ridgewood", "Central Bergen County", "prestigious village", "upscale downtown and historic homes"),
    ("River Edge", "river-edge", "Central Bergen County", "family-oriented borough", "excellent schools and parks"),
    ("River Vale", "river-vale", "Northern Bergen County", "residential township", "spacious properties and quiet streets"),
    ("Rochelle Park", "rochelle-park", "Southern Bergen County", "small township", "convenient shopping and dining"),
    ("Rockleigh", "rockleigh", "Northern Bergen County", "smallest Bergen municipality", "exclusive estates and privacy"),
    ("Rutherford", "rutherford", "Southern Bergen County", "historic borough", "Victorian architecture and cultural events"),
    ("Saddle Brook", "saddle-brook", "Southern Bergen County", "residential township", "convenient highway access"),
    ("Saddle River", "saddle-river", "Northwestern Bergen County", "exclusive borough", "estate homes and equestrian properties"),
    ("South Hackensack", "south-hackensack", "Southern Bergen County", "small township", "industrial and residential mix"),
    ("Teaneck", "teaneck", "Central Bergen County", "diverse township", "cultural diversity and community programs"),
    ("Tenafly", "tenafly", "Eastern Bergen County", "upscale borough", "excellent schools and wooded neighborhoods"),
    ("Teterboro", "teterboro", "Southern Bergen County", "airport community", "Teterboro Airport and industrial areas"),
    ("Upper Saddle River", "upper-saddle-river", "Northwestern Bergen County", "affluent borough", "luxury estates and horse farms"),
    ("Waldwick", "waldwick", "Central Bergen County", "residential borough", "family neighborhoods and local shops"),
    ("Wallington", "wallington", "Southern Bergen County", "diverse borough", "working-class heritage and community pride"),
    ("Washington Township", "washington-township", "Northern Bergen County", "residential township", "suburban character and good schools"),
    ("Westwood", "westwood", "Central Bergen County", "regional downtown center", "shopping district and restaurants"),
    ("Wood Ridge", "wood-ridge", "Southern Bergen County", "residential borough", "convenient location and community spirit"),
    ("Woodcliff Lake", "woodcliff-lake", "Northern Bergen County", "upscale borough", "corporate headquarters and reservoir"),
    ("Wyckoff", "wyckoff", "Central Bergen County", "affluent township", "colonial homes and excellent schools"),
]

def generate_unique_content(town_name, region, description, notable):
    """Generate unique Read More content for each service type."""

    content = {
        "gas_oven": f"""<h4>Wolf Gas Oven Repair in {town_name}</h4>
<p>{town_name} homeowners trust our factory-trained technicians for expert Wolf gas oven repair. As a {description} in {region}, {town_name} features many premium kitchens equipped with Wolf gas ranges. Our local technicians understand the specific needs of {town_name} residents and provide prompt, professional service.</p>
<p>Wolf gas ovens are known for their dual-stacked burners delivering 300 to 20,000 BTU precision. Common issues we repair in {town_name} include ignition failures, uneven heating, and burner problems. With {notable}, your Wolf appliance deserves the best care from certified professionals who arrive ready to diagnose and repair.</p>
<h5>Local {town_name} Service</h5>
<p>Our {town_name} service includes same-day appointments, genuine Wolf parts, and warranty-backed repairs. We service all Wolf gas oven models from 36" ranges to 60" professional units.</p>""",

        "electric_oven": f"""<h4>Wolf Electric Oven Repair in {town_name}</h4>
<p>Residents of {town_name} rely on Wolf electric ovens for consistent, precise cooking results. Our certified technicians provide comprehensive Wolf electric oven repair throughout {region}, with particular expertise serving the {description} of {town_name}.</p>
<p>Wolf electric ovens feature the dual VertiCross convection system for even heat distribution. We diagnose and repair heating element failures, control board issues, convection fan problems, and temperature inconsistencies. {town_name} customers appreciate our attention to detail and commitment to restoring their Wolf ovens to factory specifications.</p>
<h5>Expert Electric Oven Service</h5>
<p>Known for {notable}, {town_name} homes deserve premium appliance care. Our technicians stock common Wolf parts for efficient same-day repairs.</p>""",

        "induction_range": f"""<h4>Wolf Induction Range Repair in {town_name}</h4>
<p>Wolf induction ranges represent cutting-edge cooking technology, and {town_name} homeowners increasingly choose these efficient appliances. Our specialized technicians provide expert Wolf induction repair throughout {region}, serving the {description} with precision diagnostics.</p>
<p>Induction cooking uses electromagnetic heating for instant temperature response. We repair induction coil failures, error codes, control panel issues, and power module problems specific to Wolf induction systems. {town_name} residents with {notable} expect the highest level of service for their premium Wolf appliances.</p>
<h5>Specialized Induction Expertise</h5>
<p>Induction technology requires advanced training our technicians have completed. We understand Wolf's unique induction systems and provide accurate repairs.</p>""",

        "dual_fuel": f"""<h4>Wolf Dual Fuel Range Repair in {town_name}</h4>
<p>{town_name}'s discerning home chefs often choose Wolf dual fuel ranges for the best of both worlds—gas burner precision and electric oven consistency. As a {description}, {town_name} features many high-end kitchens where dual fuel ranges are the centerpiece.</p>
<p>Our {region} technicians specialize in both gas and electric systems, essential for proper dual fuel range repair. We service gas cooktop issues including ignition and burner problems, plus electric oven components like elements, sensors, and control boards. {town_name} homeowners with {notable} deserve technicians who understand these sophisticated appliances.</p>
<h5>Complete Dual Fuel Service</h5>
<p>Whether your range needs gas system repair, electric oven service, or both, our {town_name} technicians deliver comprehensive solutions.</p>""",

        "commercial": f"""<h4>Wolf Commercial Oven Repair in {town_name}</h4>
<p>Wolf commercial ovens serve serious home chefs and professional kitchens throughout {town_name}. These heavy-duty ranges require specialized service that our factory-trained technicians provide across {region}.</p>
<p>Commercial Wolf ranges feature high-BTU burners up to 35,000 BTU and robust construction for demanding use. We service high-output burner issues, heavy-duty component wear, thermostat calibration, and safety systems. {town_name}'s {description} includes discerning homeowners who demand restaurant-quality equipment and service to match.</p>
<h5>Professional-Grade Service</h5>
<p>With {notable}, {town_name} kitchens featuring Wolf commercial equipment receive the expert attention they deserve.</p>""",

        "steam_oven": f"""<h4>Wolf Steam Oven Repair in {town_name}</h4>
<p>Wolf convection steam ovens bring healthy, flavorful cooking to {town_name} kitchens. These advanced appliances combine steam and convection for superior results, and our specialized technicians provide expert repair throughout {region}.</p>
<p>Steam oven technology requires understanding of both water systems and heating elements. We repair steam generator issues, water line problems, drainage concerns, and combination mode failures. {town_name} homeowners in this {description} expect their Wolf steam ovens to perform flawlessly for artisan bread, perfectly roasted meats, and healthy vegetables.</p>
<h5>Steam Technology Experts</h5>
<p>Known for {notable}, {town_name} deserves technicians trained in Wolf's unique steam systems.</p>""",

        "range": f"""<h4>Wolf Range Repair in {town_name}</h4>
<p>Wolf ranges are the heart of premium kitchens throughout {town_name}. From 36" to 60" professional models, these ranges combine cooktops and ovens into unified cooking powerhouses. Our {region} technicians service all Wolf range configurations.</p>
<p>We provide complete range diagnostics covering all cooking surfaces and oven systems. {town_name}'s {description} features many serious home cooks who depend on their Wolf ranges daily. Common repairs include burner service, oven calibration, ignition systems, and control board replacement.</p>
<h5>Complete Range Service</h5>
<p>With {notable}, {town_name} Wolf range owners trust our comprehensive repair expertise.</p>""",

        "wall_oven": f"""<h4>Wolf Wall Oven Repair in {town_name}</h4>
<p>Wolf wall ovens bring professional cooking capabilities to {town_name} kitchens at ergonomic heights. Whether single or double configurations, these built-in ovens require expert service that our {region} technicians provide.</p>
<p>{town_name}'s {description} includes beautifully designed kitchens with Wolf wall ovens as featured appliances. We repair door mechanisms, heating elements, touch controls, display issues, and convection systems. Known for {notable}, {town_name} homeowners expect their Wolf wall ovens to deliver perfect results for every meal.</p>
<h5>Built-In Oven Specialists</h5>
<p>Wall oven installations have unique service requirements our technicians understand from years of experience.</p>"""
    }

    return content

def create_town_page(homepage_content, town_name, town_slug, region, description, notable):
    """Create a town page from the homepage template."""

    content = homepage_content

    # Replace title
    content = re.sub(
        r'<title>Wolf Appliance Repair Bergen County NJ - Authorized</title>',
        f'<title>Wolf Appliance Repair {town_name} NJ - Same-Day Service</title>',
        content
    )

    # Replace meta description
    content = re.sub(
        r'<meta name="description" content="[^"]+">',
        f'<meta name="description" content="Wolf Appliance Repair in {town_name}, NJ. Factory-certified technicians for ovens, ranges, cooktops, steam ovens. Same-day service in {region}.">',
        content
    )

    # Replace canonical
    content = re.sub(
        r'<link rel="canonical" href="https://wolfbergencounty.com/">',
        f'<link rel="canonical" href="https://wolfbergencounty.com/nj/{town_slug}/">',
        content
    )

    # Replace OG URL
    content = re.sub(
        r'<meta property="og:url" content="https://wolfbergencounty.com/">',
        f'<meta property="og:url" content="https://wolfbergencounty.com/nj/{town_slug}/">',
        content
    )

    # Replace OG title
    content = re.sub(
        r'<meta property="og:title" content="[^"]+">',
        f'<meta property="og:title" content="Wolf Appliance Repair {town_name} NJ - Same-Day Service">',
        content
    )

    # Replace schema name and URL
    content = re.sub(
        r'"name": "Wolf Appliance Repair Bergen County NJ - Authorized"',
        f'"name": "Wolf Appliance Repair {town_name} NJ"',
        content
    )
    content = re.sub(
        r'"@id": "https://wolfbergencounty.com/"',
        f'"@id": "https://wolfbergencounty.com/nj/{town_slug}/"',
        content
    )
    content = re.sub(
        r'"url": "https://wolfbergencounty.com/"',
        f'"url": "https://wolfbergencounty.com/nj/{town_slug}/"',
        content, count=1
    )

    # Replace schema addressLocality
    content = re.sub(
        r'"addressLocality": "Mahwah"',
        f'"addressLocality": "{town_name}"',
        content
    )

    # Replace hero h1
    content = re.sub(
        r'<h1>Wolf Appliance Repair Bergen County NJ - Authorized</h1>',
        f'<h1>Wolf Appliance Repair {town_name} NJ</h1>',
        content
    )

    # Replace hero p
    content = re.sub(
        r'<p>Premium Service • Factory-Trained Technicians • Serving Hackensack, Paramus, Fort Lee and all Bergen County</p>',
        f'<p>Premium Wolf Service • Factory-Trained Technicians • Same-Day Repairs in {town_name} and {region}</p>',
        content
    )

    # Replace services section h2
    content = re.sub(
        r'<h2 style="text-align:center; font-size:36px; margin-bottom:50px;">Expert Wolf Oven Repair Services</h2>',
        f'<h2 style="text-align:center; font-size:36px; margin-bottom:50px;">Expert Wolf Oven Repair in {town_name}</h2>',
        content
    )

    # Replace trust badges h2
    content = re.sub(
        r'<h2>Certified Wolf Oven Repair Service</h2>',
        f'<h2>Certified Wolf Repair in {town_name}</h2>',
        content
    )

    # Replace schedule form h2
    content = re.sub(
        r'<div class="cf-schedule-text">Schedule Your Wolf Repair Online</div>',
        f'<div class="cf-schedule-text">Schedule Wolf Repair in {town_name}</div>',
        content
    )

    # Replace address placeholder
    content = re.sub(
        r'placeholder="123 Main St, Hackensack, NJ 07601"',
        f'placeholder="123 Main St, {town_name}, NJ"',
        content
    )

    # Replace image alt texts
    content = content.replace('alt="Wolf Gas Oven Repair Bergen County NJ"', f'alt="Wolf Gas Oven Repair {town_name} NJ"')
    content = content.replace('alt="Wolf Electric Oven Repair Bergen County NJ"', f'alt="Wolf Electric Oven Repair {town_name} NJ"')
    content = content.replace('alt="Wolf Induction Range Repair Bergen County NJ"', f'alt="Wolf Induction Range Repair {town_name} NJ"')
    content = content.replace('alt="Wolf Dual Fuel Range Repair Bergen County NJ"', f'alt="Wolf Dual Fuel Range Repair {town_name} NJ"')
    content = content.replace('alt="Wolf Commercial Oven Repair Bergen County NJ"', f'alt="Wolf Commercial Oven Repair {town_name} NJ"')
    content = content.replace('alt="Wolf Steam Oven Repair Bergen County NJ"', f'alt="Wolf Steam Oven Repair {town_name} NJ"')
    content = content.replace('alt="Wolf Range Repair Bergen County NJ"', f'alt="Wolf Range Repair {town_name} NJ"')
    content = content.replace('alt="Wolf Wall Oven Repair Bergen County NJ"', f'alt="Wolf Wall Oven Repair {town_name} NJ"')

    # Fix footer Home link to go to homepage
    content = content.replace('<a href="#" class="scroll-top">Home</a>', '<a href="/">Home</a>')

    # Replace footer info
    content = re.sub(
        r'<h2>Wolf Appliance Repair Bergen County NJ</h2>',
        f'<h2>Wolf Appliance Repair {town_name} NJ</h2>',
        content
    )
    content = re.sub(
        r'<p><strong>100 Corporate Drive, Mahwah, NJ 07430</strong></p>',
        f'<p><strong>{town_name}, NJ - Bergen County</strong></p>',
        content
    )
    content = re.sub(
        r'<p>Certified Wolf oven repair serving all Bergen County towns. Same-day service available.</p>',
        f'<p>Certified Wolf oven repair serving {town_name} and all Bergen County. Same-day service available.</p>',
        content
    )

    # Fix asset paths for town subdirectory
    content = content.replace('href="assets/', 'href="/assets/')
    content = content.replace('src="assets/', 'src="/assets/')
    content = content.replace('href="favicon.png"', 'href="/favicon.png"')
    content = content.replace("url('assets/", "url('/assets/")

    # Generate unique content for Read More sections
    unique = generate_unique_content(town_name, region, description, notable)

    # Replace gas oven content
    gas_pattern = r'(<div class="content-scroll">)\s*<h4>Premium Features of Wolf Gas Ovens</h4>.*?(?=</div>\s*<div class="content-fade">)'
    content = re.sub(gas_pattern, r'\1\n                            ' + unique["gas_oven"] + '\n                            ', content, flags=re.DOTALL, count=1)

    # Replace electric oven content
    electric_pattern = r'(<div class="content-scroll">)\s*<h4>Premium Features of Wolf Electric Ovens</h4>.*?(?=</div>\s*<div class="content-fade">)'
    content = re.sub(electric_pattern, r'\1\n                            ' + unique["electric_oven"] + '\n                            ', content, flags=re.DOTALL, count=1)

    # Replace induction content
    induction_pattern = r'(<div class="content-scroll">)\s*<h4>Premium Features of Wolf Induction Ranges</h4>.*?(?=</div>\s*<div class="content-fade">)'
    content = re.sub(induction_pattern, r'\1\n                            ' + unique["induction_range"] + '\n                            ', content, flags=re.DOTALL, count=1)

    # Replace dual fuel content
    dual_pattern = r'(<div class="content-scroll">)\s*<h4>Premium Features of Wolf Dual Fuel Ranges</h4>.*?(?=</div>\s*<div class="content-fade">)'
    content = re.sub(dual_pattern, r'\1\n                            ' + unique["dual_fuel"] + '\n                            ', content, flags=re.DOTALL, count=1)

    # Replace commercial content
    commercial_pattern = r'(<div class="content-scroll">)\s*<h4>Premium Features of Wolf Commercial Ovens</h4>.*?(?=</div>\s*<div class="content-fade">)'
    content = re.sub(commercial_pattern, r'\1\n                            ' + unique["commercial"] + '\n                            ', content, flags=re.DOTALL, count=1)

    # Replace steam content
    steam_pattern = r'(<div class="content-scroll">)\s*<h4>Premium Features of Wolf Steam Ovens</h4>.*?(?=</div>\s*<div class="content-fade">)'
    content = re.sub(steam_pattern, r'\1\n                            ' + unique["steam_oven"] + '\n                            ', content, flags=re.DOTALL, count=1)

    # Replace range content
    range_pattern = r'(<div class="content-scroll">)\s*<h4>Premium Features of Wolf Ranges</h4>.*?(?=</div>\s*<div class="content-fade">)'
    content = re.sub(range_pattern, r'\1\n                            ' + unique["range"] + '\n                            ', content, flags=re.DOTALL, count=1)

    # Replace wall oven content
    wall_pattern = r'(<div class="content-scroll">)\s*<h4>Premium Features of Wolf Wall Ovens</h4>.*?(?=</div>\s*<div class="content-fade">)'
    content = re.sub(wall_pattern, r'\1\n                            ' + unique["wall_oven"] + '\n                            ', content, flags=re.DOTALL, count=1)

    return content

def create_nj_index(homepage_content):
    """Create nj/index.html with same header/footer as homepage but town grid content."""

    content = homepage_content

    # Replace title
    content = re.sub(
        r'<title>Wolf Appliance Repair Bergen County NJ - Authorized</title>',
        '<title>Wolf Appliance Repair Bergen County NJ - All Service Areas</title>',
        content
    )

    # Replace meta description
    content = re.sub(
        r'<meta name="description" content="[^"]+">',
        '<meta name="description" content="Wolf Appliance Repair serving all Bergen County NJ towns. Hackensack, Paramus, Fort Lee, Ridgewood, Teaneck and 70+ more towns.">',
        content
    )

    # Replace canonical
    content = re.sub(
        r'<link rel="canonical" href="https://wolfbergencounty.com/">',
        '<link rel="canonical" href="https://wolfbergencounty.com/nj/">',
        content
    )

    # Replace OG URL
    content = re.sub(
        r'<meta property="og:url" content="https://wolfbergencounty.com/">',
        '<meta property="og:url" content="https://wolfbergencounty.com/nj/">',
        content
    )

    # Replace hero h1
    content = re.sub(
        r'<h1>Wolf Appliance Repair Bergen County NJ - Authorized</h1>',
        '<h1>Wolf Appliance Repair - All Bergen County NJ Towns</h1>',
        content
    )

    # Replace hero p
    content = re.sub(
        r'<p>Premium Service • Factory-Trained Technicians • Serving Hackensack, Paramus, Fort Lee and all Bergen County</p>',
        '<p>Factory-Certified Technicians • Same-Day Service • Select Your Town Below</p>',
        content
    )

    # Fix asset paths
    content = content.replace('href="assets/', 'href="/assets/')
    content = content.replace('src="assets/', 'src="/assets/')
    content = content.replace('href="favicon.png"', 'href="/favicon.png"')
    content = content.replace("url('assets/", "url('/assets/")

    return content


def main():
    # Read homepage template
    with open('/private/tmp/wolf-bergen-county/index.html', 'r', encoding='utf-8') as f:
        homepage = f.read()

    base_dir = '/private/tmp/wolf-bergen-county/nj'

    # Generate nj/index.html
    nj_index = create_nj_index(homepage)
    with open(os.path.join(base_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(nj_index)
    print("Generated: nj/index.html")

    for town_name, town_slug, region, description, notable in TOWNS:
        # Create directory
        town_dir = os.path.join(base_dir, town_slug)
        os.makedirs(town_dir, exist_ok=True)

        # Generate page
        page_content = create_town_page(homepage, town_name, town_slug, region, description, notable)

        # Write file
        filepath = os.path.join(town_dir, 'index.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page_content)

        print(f"Generated: {town_slug}")

    print(f"\nGenerated {len(TOWNS)} town pages with unique content.")

if __name__ == "__main__":
    main()
