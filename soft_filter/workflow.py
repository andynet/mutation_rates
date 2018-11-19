from gwf import Workflow
from templates import vcf_filter, vcf_tabix

gwf = Workflow()

raw_vcf = ''
known_vcf = ''

gwf.target(
    f'{}',
    inputs=[],
    outputs=[],
    options={},
) << f'''

'''

tmp = vcf_filter(raw_vcf)
gwf.target_from_template('vcf_filter.{}'.format(raw_vcf), tmp)

tmp = vcf_tabix(tmp[1])
gwf.target_from_template(f'{}', tmp)

